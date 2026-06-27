import os
import sys
import json
import urllib.parse
import re
from datetime import datetime, timedelta

# In WAGI, files are read relative to the root of the sandbox volumes
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DATA_PATH = os.path.join(BASE_DIR, 'models', 'model_data.json')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'src', 'templates', 'index.html')
STATIC_DIR = os.path.join(BASE_DIR, 'src', 'static')

def log(msg):
    # Print to stderr for WAGI execution logs
    sys.stderr.write(f"[WAGI APP LOG] {msg}\n")
    sys.stderr.flush()

def load_model_data():
    if not os.path.exists(MODEL_DATA_PATH):
        raise FileNotFoundError(f"Model data file not found at {MODEL_DATA_PATH}. Run export_model.py first.")
    with open(MODEL_DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def render_home(model_data):
    if not os.path.exists(TEMPLATE_PATH):
        return serve_error(404, f"Template file not found at {TEMPLATE_PATH}")

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Get states and commodities sorted
    states = sorted(list(model_data['location_tree'].keys()))
    commodities = sorted(list(model_data['commodity_tree'].keys()))

    # Simulating the Flask template url_for and loops:
    # 1. Replace static file url_for patterns (e.g. {{ url_for('static', filename='...') }})
    html = re.sub(
        r'\{\{\s*url_for\(\s*\'static\'\s*,\s*filename\s*=\s*[\'"]([^\'"]+)[\'"]\s*\)\s*\}\}',
        r'/static/\1',
        html
    )

    # 2. Render state options dynamically matching the Jinja2 loop pattern robustly
    state_options = []
    for s in states:
        state_options.append(f'<option value="{s}">{s}</option>')
    
    state_pattern = r'\{%\s*for\s+state\s+in\s+states\s*%\}.*?\{%\s*endfor\s*\%}'
    html = re.sub(state_pattern, "\n".join(state_options), html, flags=re.DOTALL)

    # 3. Render commodity options dynamically matching the Jinja2 loop pattern robustly
    commodity_options = []
    for c in commodities:
        commodity_options.append(f'<option value="{c}">{c}</option>')
        
    commodity_pattern = r'\{%\s*for\s+commodity\s+in\s+commodities\s*%\}.*?\{%\s*endfor\s*\%}'
    html = re.sub(commodity_pattern, "\n".join(commodity_options), html, flags=re.DOTALL)

    # Output HTTP headers and content
    print("Content-Type: text/html; charset=utf-8")
    print(f"Content-Length: {len(html.encode('utf-8'))}")
    print("") # Blank line separating headers and body
    sys.stdout.write(html)
    sys.stdout.flush()

def serve_static(path):
    # Convert all backslashes to forward slashes for uniform processing
    normalized_path = path.replace('\\', '/')
    clean_path = normalized_path.lstrip('/')
    
    # Remove 'static/' prefix if present
    if clean_path.startswith('static/'):
        clean_path = clean_path[7:]

    # Security check: prevent directory traversal
    full_path = os.path.normpath(os.path.join(STATIC_DIR, clean_path))
    
    if not full_path.startswith(STATIC_DIR) or not os.path.isfile(full_path):
        return serve_error(404, f"Static file not found: {path}")

    # Determine MIME type
    mime_type = "text/plain"
    if full_path.endswith(".css"):
        mime_type = "text/css"
    elif full_path.endswith(".js"):
        mime_type = "application/javascript"

    try:
        with open(full_path, 'rb') as f:
            content = f.read()
        print(f"Content-Type: {mime_type}")
        print(f"Content-Length: {len(content)}")
        print("")
        sys.stdout.buffer.write(content)
        sys.stdout.buffer.flush()
    except Exception as e:
        return serve_error(500, f"Error reading static file: {str(e)}")

def serve_json(data):
    body = json.dumps(data)
    body_bytes = body.encode('utf-8')
    print("Content-Type: application/json")
    print(f"Content-Length: {len(body_bytes)}")
    print("")
    sys.stdout.write(body)
    sys.stdout.flush()

def serve_error(code, message):
    res = {"success": False, "error": message}
    body = json.dumps(res)
    body_bytes = body.encode('utf-8')
    print(f"Status: {code}")
    print("Content-Type: application/json")
    print(f"Content-Length: {len(body_bytes)}")
    print("")
    sys.stdout.write(body)
    sys.stdout.flush()

def read_post_body():
    try:
        content_length = int(os.environ.get('CONTENT_LENGTH', 0))
        if content_length > 0:
            body = sys.stdin.read(content_length)
            return json.loads(body)
    except Exception as e:
        log(f"Error reading body: {str(e)}")
    return {}

def calculate_prediction(model_data, request_data, min_price_factor=1.0, max_price_factor=1.0):
    coefs = model_data['coefs']
    intercept = model_data['intercept']
    feature_names = model_data['feature_names']
    avg_prices = model_data['avg_prices']

    market = request_data['market']
    commodity = request_data['commodity']
    variety = request_data['variety']
    grade = request_data['grade']

    # 1. Lookup average historical min/max prices
    key = f"{market}||{commodity}||{variety}||{grade}"
    if key in avg_prices:
        avg_min = avg_prices[key]['avg_min']
        avg_max = avg_prices[key]['avg_max']
    else:
        avg_min = 100.0
        avg_max = 200.0

    avg_min *= min_price_factor
    avg_max *= max_price_factor

    # 2. Build feature vector map
    # Categories columns for dummy representation
    inputs = {
        'Min_x0020_Price': avg_min,
        'Max_x0020_Price': avg_max,
        f"State_{request_data['state']}": 1.0,
        f"District_{request_data['district']}": 1.0,
        f"Market_{market}": 1.0,
        f"Commodity_{commodity}": 1.0,
        f"Variety_{variety}": 1.0,
        f"Grade_{grade}": 1.0
    }

    # 3. Calculate dot product: Sum(X_i * W_i) + Intercept
    pred = intercept
    for name, coef in zip(feature_names, coefs):
        if name in inputs:
            pred += inputs[name] * coef

    return float(pred)

def handle_request():
    path = os.environ.get('PATH_INFO', '/')
    method = os.environ.get('REQUEST_METHOD', 'GET').upper()
    log(f"Handling {method} {path}")

    # Load compiled model and data once
    try:
        model_data = load_model_data()
    except Exception as e:
        return serve_error(500, f"Error loading model data: {str(e)}")

    # Route: Home Page
    if path == '/' or path == '/index.html':
        return render_home(model_data)

    # Route: Static Assets
    elif path.startswith('/static/'):
        return serve_static(path)

    # Route: Get Districts (POST)
    elif path == '/get_districts' and method == 'POST':
        body = read_post_body()
        state = body.get('state', '')
        districts = sorted(list(model_data['location_tree'].get(state, {}).keys()))
        return serve_json(districts)

    # Route: Get Markets (POST)
    elif path == '/get_markets' and method == 'POST':
        body = read_post_body()
        district = body.get('district', '')
        
        # Traverse tree to find the district
        markets = []
        for state, districts in model_data['location_tree'].items():
            if district in districts:
                markets.extend(districts[district])
        markets = sorted(list(set(markets)))
        return serve_json(markets)

    # Route: Get Varieties (POST)
    elif path == '/get_varieties' and method == 'POST':
        body = read_post_body()
        commodity = body.get('commodity', '')
        varieties = sorted(list(model_data['commodity_tree'].get(commodity, {}).keys()))
        return serve_json(varieties)

    # Route: Get Grades (POST)
    elif path == '/get_grades' and method == 'POST':
        body = read_post_body()
        variety = body.get('variety', '')
        
        # Traverse tree to find the variety
        grades = []
        for commodity, varieties in model_data['commodity_tree'].items():
            if variety in varieties:
                grades.extend(varieties[variety])
        grades = sorted(list(set(grades)))
        return serve_json(grades)

    # Route: Predict (POST)
    elif path == '/predict' and method == 'POST':
        body = read_post_body()
        
        try:
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            tomorrow = today + timedelta(days=1)

            # Predict for today (1.0 factor), yesterday (0.95 factor), tomorrow (1.05 factor)
            today_price = calculate_prediction(model_data, body, 1.0, 1.0)
            yesterday_price = calculate_prediction(model_data, body, 0.95, 0.95)
            tomorrow_price = calculate_prediction(model_data, body, 1.05, 1.05)

            # Historical price lookup
            key = f"{body['market']}||{body['commodity']}||{body['variety']}||{body['grade']}"
            if key in model_data['price_history']:
                historical_prices = model_data['price_history'][key]['prices']
                historical_dates = model_data['price_history'][key]['dates']
            else:
                historical_prices = []
                historical_dates = []

            return serve_json({
                'success': True,
                'today_price': round(today_price, 2),
                'yesterday_price': round(yesterday_price, 2),
                'tomorrow_price': round(tomorrow_price, 2),
                'today_date': today.strftime('%Y-%m-%d'),
                'yesterday_date': yesterday.strftime('%Y-%m-%d'),
                'tomorrow_date': tomorrow.strftime('%Y-%m-%d'),
                'historical_prices': historical_prices,
                'historical_dates': historical_dates
            })
        except Exception as e:
            return serve_error(500, f"Prediction failed: {str(e)}")

    else:
        return serve_error(404, f"Endpoint not found: {path}")

if __name__ == '__main__':
    handle_request()
