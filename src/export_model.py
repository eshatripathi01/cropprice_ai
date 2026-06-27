import os
import json
import pandas as pd
import joblib

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'data', 'dataset.csv')
    model_path = os.path.join(base_dir, 'models', 'linear_regression_model.pkl')
    output_json_path = os.path.join(base_dir, 'models', 'model_data.json')

    print("Loading model and dataset...")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please train the model first.")
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at {dataset_path}.")

    model = joblib.load(model_path)
    df = pd.read_csv(dataset_path)

    # 1. Extract linear regression parameters
    coefs = list(model.coef_)
    intercept = float(model.intercept_)
    feature_names = list(model.feature_names_in_)

    print(f"Model has {len(feature_names)} features.")

    # 2. Compute dropdown menus data and cascading dropdown relationships
    # We want a tree-like structure: State -> District -> Market
    # And Commodity -> Variety -> Grade
    print("Building cascading relationship maps...")
    
    # State -> District -> Market tree
    location_tree = {}
    for (state, district, market), _ in df.groupby(['State', 'District', 'Market']):
        if state not in location_tree:
            location_tree[state] = {}
        if district not in location_tree[state]:
            location_tree[state][district] = []
        if market not in location_tree[state][district]:
            location_tree[state][district].append(market)

    # Commodity -> Variety -> Grade tree
    commodity_tree = {}
    for (commodity, variety, grade), _ in df.groupby(['Commodity', 'Variety', 'Grade']):
        if commodity not in commodity_tree:
            commodity_tree[commodity] = {}
        if variety not in commodity_tree[commodity]:
            commodity_tree[commodity][variety] = []
        if grade not in commodity_tree[commodity][variety]:
            commodity_tree[commodity][variety].append(grade)

    # 3. Calculate average Min and Max prices for each (Market, Commodity, Variety, Grade) combination
    # This avoids using pandas to calculate means at runtime.
    print("Calculating historical averages for all crop combinations...")
    avg_prices = {}
    grouped = df.groupby(['Market', 'Commodity', 'Variety', 'Grade'])
    for name, group in grouped:
        market, commodity, variety, grade = name
        avg_min = float(group['Min_x0020_Price'].mean())
        avg_max = float(group['Max_x0020_Price'].mean())
        
        # Create a unique key for lookup
        key = f"{market}||{commodity}||{variety}||{grade}"
        avg_prices[key] = {
            'avg_min': avg_min,
            'avg_max': avg_max
        }

    # Also compute historical prices/dates list for visualization (last 30 records for each crop combination)
    print("Extracting historical price lists for visual charts...")
    historical_price_history = {}
    for name, group in grouped:
        market, commodity, variety, grade = name
        sorted_group = group.sort_values('Arrival_Date')
        
        # Get modal prices and arrival dates (up to last 30)
        prices = [float(p) for p in sorted_group['Modal_x0020_Price'].tolist()[-30:]]
        dates = [str(d) for d in sorted_group['Arrival_Date'].tolist()[-30:]]
        
        key = f"{market}||{commodity}||{variety}||{grade}"
        historical_price_history[key] = {
            'prices': prices,
            'dates': dates
        }

    # 4. Save everything to a structured JSON file
    model_data = {
        'coefs': coefs,
        'intercept': intercept,
        'feature_names': feature_names,
        'location_tree': location_tree,
        'commodity_tree': commodity_tree,
        'avg_prices': avg_prices,
        'price_history': historical_price_history
    }

    print(f"Writing all data to {output_json_path}...")
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(model_data, f, indent=2)

    print("Model and metadata successfully exported for WebAssembly/WAGI use!")

if __name__ == '__main__':
    main()
