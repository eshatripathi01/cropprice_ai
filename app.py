from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the trained model
model = joblib.load('linear_regression_model.pkl')

# Load the full dataset for dropdowns and historical data
df = pd.read_csv('9ef84268-d588-465a-a308-a864a43d0070.csv')

# Create a sample for faster operations
df_sample = df.copy()

# Drop the 'Arrival_Date' column as it was done during training
df_sample = df_sample.drop('Arrival_Date', axis=1)

# Get the list of categorical columns
categorical_cols = ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']

@app.route('/')
def home():
    # Get unique values for each categorical column for the dropdown menus
    states = sorted(df_sample['State'].unique())
    commodities = sorted(df_sample['Commodity'].unique())
    
    return render_template('index.html', states=states, commodities=commodities)

@app.route('/get_districts', methods=['POST'])
def get_districts():
    state = request.json['state']
    districts = sorted(df_sample[df_sample['State'] == state]['District'].unique())
    return jsonify(districts)

@app.route('/get_markets', methods=['POST'])
def get_markets():
    district = request.json['district']
    markets = sorted(df_sample[df_sample['District'] == district]['Market'].unique())
    return jsonify(markets)

@app.route('/get_varieties', methods=['POST'])
def get_varieties():
    commodity = request.json['commodity']
    varieties = sorted(df_sample[df_sample['Commodity'] == commodity]['Variety'].unique())
    return jsonify(varieties)

@app.route('/get_grades', methods=['POST'])
def get_grades():
    variety = request.json['variety']
    grades = sorted(df_sample[df_sample['Variety'] == variety]['Grade'].unique())
    return jsonify(grades)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        data = request.json
        
        # Get current date and calculate yesterday and tomorrow
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        # Create a DataFrame with the input data for today's price
        # Use average min and max prices from historical data if available
        market = data['market']
        commodity = data['commodity']
        variety = data['variety']
        grade = data['grade']
        
        # Get historical data for the selected crop
        historical_data = df[(df['Market'] == market) & 
                           (df['Commodity'] == commodity) & 
                           (df['Variety'] == variety) & 
                           (df['Grade'] == grade)].sort_values('Arrival_Date')
        
        # Calculate average min and max prices from historical data
        if not historical_data.empty:
            avg_min_price = historical_data['Min_x0020_Price'].mean()
            avg_max_price = historical_data['Max_x0020_Price'].mean()
        else:
            # Default values if no historical data
            avg_min_price = 100
            avg_max_price = 200
        
        # Create input dataframe for prediction
        input_df = pd.DataFrame({
            'State': [data['state']],
            'District': [data['district']],
            'Market': [market],
            'Commodity': [commodity],
            'Variety': [variety],
            'Grade': [grade],
            'Min_x0020_Price': [avg_min_price],
            'Max_x0020_Price': [avg_max_price]
        })
        
        # Apply one-hot encoding to match the training data format
        input_encoded = pd.get_dummies(input_df, columns=categorical_cols)
        
        # Align the input data with the model's expected features
        missing_cols = set(model.feature_names_in_) - set(input_encoded.columns)
        for col in missing_cols:
            input_encoded[col] = 0
        
        # Ensure columns are in the same order as during training
        input_encoded = input_encoded[model.feature_names_in_]
        
        # Make prediction for today's price
        today_prediction = model.predict(input_encoded)[0]
        
        # Slightly modify min/max prices for yesterday and tomorrow to simulate price changes
        # For yesterday's prediction (slightly lower)
        input_df_yesterday = input_df.copy()
        input_df_yesterday['Min_x0020_Price'] = input_df_yesterday['Min_x0020_Price'] * 0.95
        input_df_yesterday['Max_x0020_Price'] = input_df_yesterday['Max_x0020_Price'] * 0.95
        
        # Apply encoding for yesterday
        yesterday_encoded = pd.get_dummies(input_df_yesterday, columns=categorical_cols)
        for col in missing_cols:
            yesterday_encoded[col] = 0
        yesterday_encoded = yesterday_encoded[model.feature_names_in_]
        yesterday_prediction = model.predict(yesterday_encoded)[0]
        
        # For tomorrow's prediction (slightly higher)
        input_df_tomorrow = input_df.copy()
        input_df_tomorrow['Min_x0020_Price'] = input_df_tomorrow['Min_x0020_Price'] * 1.05
        input_df_tomorrow['Max_x0020_Price'] = input_df_tomorrow['Max_x0020_Price'] * 1.05
        
        # Apply encoding for tomorrow
        tomorrow_encoded = pd.get_dummies(input_df_tomorrow, columns=categorical_cols)
        for col in missing_cols:
            tomorrow_encoded[col] = 0
        tomorrow_encoded = tomorrow_encoded[model.feature_names_in_]
        tomorrow_prediction = model.predict(tomorrow_encoded)[0]
        
        # If historical data exists, prepare it for the chart
        if not historical_data.empty:
            # Get the last 30 days of data or all available data if less than 30 days
            historical_prices = historical_data['Modal_x0020_Price'].tolist()[-30:]
            
            # Use actual arrival dates from the dataset if available
            if 'Arrival_Date' in historical_data.columns:
                historical_dates = historical_data['Arrival_Date'].tolist()[-30:]
            else:
                # Generate dates if arrival dates not available
                historical_dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30, 0, -1)]
                
                # Ensure the lengths match (if less than 30 days of data)
                if len(historical_prices) < 30:
                    historical_dates = historical_dates[-len(historical_prices):]
        else:
            # If no historical data, provide empty lists
            historical_prices = []
            historical_dates = []
        
        # Return prediction results and historical data
        return jsonify({
            'success': True,
            'today_price': round(today_prediction, 2),
            'yesterday_price': round(yesterday_prediction, 2),
            'tomorrow_price': round(tomorrow_prediction, 2),
            'today_date': today.strftime('%Y-%m-%d'),
            'yesterday_date': yesterday.strftime('%Y-%m-%d'),
            'tomorrow_date': tomorrow.strftime('%Y-%m-%d'),
            'historical_prices': historical_prices,
            'historical_dates': historical_dates
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)