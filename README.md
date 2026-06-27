# Crop Price Predictor AI Web Application

An interactive web application that uses a trained machine learning model to predict crop prices based on location, crop type, variety, and grade. The application features a clean Model-View-Controller (MVC) directory layout, consolidated frontend assets, system-integrated dark mode, and an interactive price trend visualization.

---

## Project Structure

The project has been restructured to separate data, model binaries, source code, and static assets:

```text
cropprice_ai/
├── data/
│   └── dataset.csv                     # The raw crop price dataset
├── models/
│   └── linear_regression_model.pkl     # The trained scikit-learn model binary
├── src/
│   ├── app.py                          # The Flask web application server
│   ├── train.py                        # The model training pipeline script
│   ├── static/                         # Static assets served by Flask
│   │   ├── css/
│   │   │   └── style.css               # Consolidated stylesheets (variables, layout, dark mode)
│   │   └── js/
│   │       └── script.js               # Consolidated JS (dropdowns, Chart.js, animations, tooltips)
│   └── templates/
│       └── index.html                  # Clean HTML interface (linked to static assets)
├── requirements.txt                    # Python dependencies
└── README.md                           # Documentation
```

---

## Features

* **MVC Restructuring:** Clean separation of concerns separating source code, data, and models.
* **Refactored ML Training Pipeline:** Corrected out-of-order execution script that preprocesses, trains, evaluates, and exports the model sequentially.
* **Cascading Dynamic Dropdowns:** Dropdowns (State $\rightarrow$ District $\rightarrow$ Market and Commodity $\rightarrow$ Variety $\rightarrow$ Grade) automatically load and filter options from the dataset.
* **Linear Price Trend Chart:** Renders a 3-day line chart (Yesterday, Today, and Tomorrow) showing the simulated price direction, preventing empty chart displays.
* **Absolute Path Resolution:** Uses robust file path resolution so the application can be run from any working directory without path failures.
* **Dark Mode Support:** Auto-detects system preferences and switches layout colors dynamically.
* **Polished UX:** Includes custom scrollbars, card hover micro-animations, scroll-based fade-in effects, and informative feature card tooltips.

---

## Installation & Setup

### Prerequisites
* Python 3.8 or higher installed on your system.
* Pip (Python package manager).

### 1. Clone or Open the Project
Ensure you are in the project root directory:
```bash
cd d:\CropPriceAI\cropprice_ai
```

### 2. Set Up a Virtual Environment (Recommended)
Creating a virtual environment prevents package conflicts:

* **On Windows:**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
Install all required libraries from `requirements.txt`:
```bash
python -m pip install -r requirements.txt
```
*(Dependencies include: `flask`, `pandas`, `numpy`, `scikit-learn`, and `joblib`)*

---

## Step-by-Step Usage Guide

### Step 1: Train the Machine Learning Model
Before running the web app, you must train the linear regression model. The pipeline loads the dataset, cleans it, applies one-hot encoding, trains the model, and exports it to the `models/` directory.

Run the training script:
```bash
python src/train.py
```

**Expected Console Output:**
```text
Starting crop price model training pipeline...
Loading dataset from: D:\CropPriceAI\cropprice_ai\data\dataset.csv
Dataset loaded. Shape: (17628, 10)
Dropped 'Arrival_Date' column.
Applying one-hot encoding to categorical features...
Preprocessed dataset shape: (17628, 2671)
Training set size: 14102 samples
Testing set size: 3526 samples
Training Linear Regression model...
Model training complete.
Evaluating model performance...
Mean Squared Error (MSE): 329999.37
R-squared (R2) Score: 0.9896
Exporting trained model to: D:\CropPriceAI\cropprice_ai\models\linear_regression_model.pkl
Model successfully saved.
Verifying exported model...
Verification prediction success. Predicted price: 1332.61
```

### Step 2: Start the Web Application Server
Launch the Flask development server:
```bash
python src/app.py
```

**Expected Console Output:**
```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 3: Run and Predict
1. Open your web browser and navigate to **`http://127.0.0.1:5000`**.
2. Select your geographical parameters:
   * Choose a **State**. This dynamically activates and filters the **District** dropdown.
   * Choose a **District**. This dynamically activates and filters the **Market** dropdown.
3. Select your agricultural parameters:
   * Choose a **Commodity** (crop). This dynamically activates and filters the **Variety** dropdown.
   * Choose a **Variety**. This dynamically activates and filters the **Grade** dropdown.
4. Click **Predict Price**.
5. View the predicted prices for Yesterday, Today, and Tomorrow, and explore the **Predicted Modal Price Trend** line chart below.

---

## Technical Details

### Linear Price Trend Simulation
Because the underlying dataset contains records from a single unique date (`11-09-2025`), there is no historical time-series data available. To show a price direction:
* **Today's Price:** The model makes a baseline prediction using average min/max historical values for that combination.
* **Yesterday's Price:** Simulated by scaling the min/max feature values down by 5% ($0.95 \times$ price) and running the model.
* **Tomorrow's Price:** Simulated by scaling the min/max feature values up by 5% ($1.05 \times$ price) and running the model.
* These three values are plotted on the Chart.js line chart to visualize the predicted slope.