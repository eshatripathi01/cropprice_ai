# Crop Price Predictor Web Application

## Overview

This web application uses a trained linear regression model to predict crop prices based on various factors such as location, crop type, variety, and grade. The application provides a modern, responsive user interface with interactive features for data visualization.

## Features

- **Crop Price Prediction**: Predict crop prices using a trained machine learning model
- **Interactive UI**: Modern, responsive design with Bootstrap
- **Dynamic Dropdowns**: Cascading dropdowns for state, district, market, commodity, variety, and grade
- **Data Visualization**: Historical price trends displayed using Chart.js
- **Price Statistics**: Display of yesterday's, today's, and tomorrow's prices
- **Dark Mode Support**: Automatic dark mode based on system preferences
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Project Structure

```
crop_ai/
├── app.py                  # Flask application
├── linear_regression_model.pkl  # Trained model
├── 9ef84268-d588-465a-a308-a864a43d0070.csv  # Dataset
├── crop_price.py           # Original model training code
├── requirements.txt        # Project dependencies
├── static/                 # Static files
│   ├── style.css           # Custom CSS
│   └── script.js           # Custom JavaScript
└── templates/              # HTML templates
    └── index.html          # Main application page
```

## Installation

1. Ensure you have Python installed (version 3.6 or higher)
2. Install the required dependencies:

```bash
python -m pip install flask pandas numpy joblib scikit-learn
```

## Running the Application

1. Navigate to the project directory:

```bash
cd path/to/crop_ai
```

2. Run the Flask application:

```bash
python app.py
```

3. Open your web browser and go to http://127.0.0.1:5000

## Usage

1. Select the state, district, market, commodity, variety, and grade from the dropdown menus
2. Click the "Predict Price" button
3. View yesterday's, today's, and tomorrow's prices along with the historical price chart

## Model Information

The application uses a linear regression model trained on historical crop price data. The model takes into account various factors such as location, crop type, variety, and grade to predict crop prices.

## Troubleshooting

- If you encounter a version warning about the model, you may need to retrain the model using the same scikit-learn version as your installation
- If the application fails to start, ensure all dependencies are installed correctly
- If you encounter Chart.js errors related to canvas reuse, the application includes a fix that properly destroys and recreates chart instances
- For any other issues, check the console output for error messages

## Future Improvements

- Add user authentication for personalized predictions
- Implement more advanced machine learning models
- Add export functionality for prediction results
- Integrate with external APIs for real-time market data
- Add multi-language support

## License

This project is licensed under the MIT License - see the LICENSE file for details.