import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def main():
    # 1. Resolve absolute paths dynamically relative to this script's location
    # src/train.py is inside src/, so its parent is the project root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, 'data', 'dataset.csv')
    model_dir = os.path.join(base_dir, 'models')
    model_path = os.path.join(model_dir, 'linear_regression_model.pkl')

    print("Starting crop price model training pipeline...")
    print(f"Loading dataset from: {dataset_path}")

    # Ensure the data folder and file exist
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}.")

    # 2. Load the dataset
    df = pd.read_csv(dataset_path)
    print(f"Dataset loaded. Shape: {df.shape}")

    # 3. Explore data (basic checks)
    print("\nColumns and null counts:")
    print(df.isnull().sum())

    # 4. Preprocess the data
    # Drop the 'Arrival_Date' column as it contains a single non-informative date
    if 'Arrival_Date' in df.columns:
        df = df.drop('Arrival_Date', axis=1)
        print("\nDropped 'Arrival_Date' column.")

    # Identify categorical columns for one-hot encoding
    categorical_cols = ['State', 'District', 'Market', 'Commodity', 'Variety', 'Grade']
    
    # Apply one-hot encoding matching the original training parameters (drop_first=True)
    print("Applying one-hot encoding to categorical features...")
    df_processed = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    print(f"Preprocessed dataset shape: {df_processed.shape}")

    # 5. Split the data into features (X) and target (y)
    X = df_processed.drop('Modal_x0020_Price', axis=1)
    y = df_processed['Modal_x0020_Price']

    # Split into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set size: {X_train.shape[0]} samples")
    print(f"Testing set size: {X_test.shape[0]} samples")

    # 6. Train the Linear Regression model
    print("\nTraining Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("Model training complete.")

    # 7. Evaluate the model
    print("\nEvaluating model performance...")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"R-squared (R2) Score: {r2:.4f}")

    # 8. Export the model binary
    os.makedirs(model_dir, exist_ok=True)
    print(f"\nExporting trained model to: {model_path}")
    joblib.dump(model, model_path)
    print("Model successfully saved.")

    # 9. Verify the exported model by running a sample prediction
    print("\nVerifying exported model...")
    loaded_model = joblib.load(model_path)
    sample_input = X_test.iloc[[0]]  # Keep as a DataFrame to retain feature names
    sample_pred = loaded_model.predict(sample_input)
    print(f"Verification prediction success. Predicted price: {sample_pred[0]:.2f}")

if __name__ == '__main__':
    main()
