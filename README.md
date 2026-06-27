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
* **Tomorrow's Price:** Simulated by scaling the min/max feature values up by 5% ($1.05 \times$ price) and running the model.
* These three values are plotted on the Chart.js line chart to visualize the predicted slope.
