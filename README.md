# 🌾 Crop Price Predictor AI 🚀

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![ML Library](https://img.shields.io/badge/ML-scikit--learn-orange.svg)](https://scikit-learn.org/)

An interactive, data-driven web application designed to bridge the gap between complex machine learning and everyday agricultural decision-making. By leveraging a trained linear regression model, this tool empowers users to predict regional crop prices based on location, crop type, variety, and grade. 

Featuring a modern **Model-View-Controller (MVC)** architecture, a dynamic cascading frontend, system-integrated dark mode, and an intuitive simulated price trend visualizer, this project turns raw data into actionable insights.

---

## 🏗️ Project Architecture

The project is structured with a strict separation of concerns, keeping data, model logic, and presentation assets beautifully organized:

```text
cropprice_ai/
├── data/
│   └── dataset.csv                     # Raw agricultural market dataset
├── models/
│   └── linear_regression_model.pkl     # Serialized scikit-learn model binary
├── src/
│   ├── app.py                          # Flask web application server (Controller)
│   ├── train.py                        # End-to-end ML training pipeline script
│   ├── static/                         # Static assets served by Flask
│   │   ├── css/
│   │   │   └── style.css               # UI variables, layout structure, & dark mode media queries
│   │   └── js/
│   │       └── script.js               # Dynamic dropdown logic, Chart.js, & UI animations
│   └── templates/
│       └── index.html                  # Clean, semantic HTML5 user interface (View)
├── requirements.txt                    # Python package dependencies
└── README.md                           # Project documentation
```

---

## ✨ Core Features

* **🧼 Clean MVC Restructuring:** Clear, professional codebase separation separating backend processing from frontend presentation.
* **🔄 Sequential ML Pipeline:** A robust training script that handles preprocessing, one-hot encoding, model fitting, evaluation, and export flawlessly in order.
* **🌊 Cascading Dynamic Dropdowns:** Smart filtering that updates in real-time (`State` → `District` → `Market` and `Commodity` → `Variety` → `Grade`), ensuring users never pick an invalid data combination.
* **📊 3-Day Price Trend Simulation:** Renders a clean line chart mapping *Yesterday, Today, and Tomorrow* to help visualize price trajectories directly via Chart.js.
* **🌍 Absolute Path Resolution:** Built using robust path handling, allowing you to spin up the application smoothly from any working directory without breaking file references.
* **🌙 Native Dark Mode Support:** Automatically syncs with the user's operating system preferences for a premium look.
* **✨ Polished UX Micro-interactions:** Fluid card hover effects, custom scrollbars, scroll-fades, and helpful feature tooltips.

---

## ⚙️ Installation & Setup

### Prerequisites

* **Python 3.8 or higher** installed.
* **Pip** (Python package manager).

### 1. Clone & Navigate

Open your terminal and ensure you are in the project root directory:

```bash
cd d:\CropPriceAI\cropprice_ai

```

### 2. Set Up a Virtual Environment (Recommended)

Isolate your project dependencies to prevent version conflicts:

* **Windows:**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1

```


* **macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```



### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt

```

*(Installs: `flask`, `pandas`, `numpy`, `scikit-learn`, and `joblib`)*

---

## 🚀 Step-by-Step Usage Guide

### Step 1: Train the Machine Learning Model 🧠

Before launching the web app, fire up the training pipeline. The script loads the dataset, applies one-hot encoding to handle categorical features, fits the linear regression model, and exports the binary.

```bash
python src/train.py

```

<details>
<summary><b>📈 Click to view expected training console output</b></summary>

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

</details>

### Step 2: Spin Up the Web Server 🌐

Launch the Flask development server to bring the application to life:

```bash
python src/app.py

```

*Expected output:*

```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)

```

### Step 3: Run & Predict 🔮

1. Open your browser and head to **`http://127.0.0.1:5000`**.
2. **Select Location:** Pick a *State*, which dynamically unlocks and filters the *District*, followed by the local *Market*.
3. **Select Produce:** Choose the *Commodity*, then filter down to its specific *Variety* and *Grade*.
4. Hit **Predict Price** to see your results instantly mapped onto the interactive line chart!

---

## 🛠️ Behind the Scenes: Price Trend Simulation

> **Note on Data Strategy:**
> Because the underlying dataset contains marketplace snapshots from a single unique date (`11-09-2025`), authentic time-series forecasting isn't possible.

To overcome this limitation and provide an interactive chart direction for users, a clever **feature-scaling simulation** was engineered:

* **Today's Price ($P$):** The baseline prediction generated directly by the model using actual dataset metrics.
* **Yesterday's Price:** Simulated by scaling down the min/max features by $5\%$ ($0.95 \times P$) before passing them to the model.
* **Tomorrow's Price:** Simulated by scaling up the min/max features by $5\%$ ($1.05 \times P$) before passing them to the model.

This mathematical slope provides a clean, visual direction of potential market shifts based on feature weight bounds.

---

Made with ❤️ for smarter agriculture.

