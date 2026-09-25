import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# --- 1. Dataset Generation ---
def generate_smart_grid_dataset(n_samples: int = 1200, random_seed: int = 42) -> pd.DataFrame:
    np.random.seed(random_seed)
    temp = np.clip(np.random.normal(loc=30.0, scale=6.0, size=n_samples), 12.0, 48.0)
    util = np.random.uniform(low=10.0, high=95.0, size=n_samples)
    chiller_base = 0.45 * temp + 0.35 * util
    chiller_noise = np.random.normal(loc=0.0, scale=2.5, size=n_samples)
    chiller = np.clip(chiller_base + chiller_noise, 5.0, 75.0)
    uptime = np.clip(np.random.exponential(scale=150.0, size=n_samples), 1.0, 720.0)
    noise = np.random.normal(loc=0.0, scale=4.0, size=n_samples)

    total_power = (
        45.0
        + 1.25 * temp
        + 3.80 * util
        + 2.10 * chiller
        + 0.05 * uptime
        + noise
    )

    return pd.DataFrame({
        "Ambient_Temp_C": np.round(temp, 2),
        "Cluster_Utilization_Pct": np.round(util, 2),
        "Chiller_Demand_kW": np.round(chiller, 2),
        "Uptime_Hours": np.round(uptime, 1),
        "Total_Power_kW": np.round(total_power, 2)
    })


# --- 2. Custom Linear Regression Class ---
class CustomLinearRegression:
    def __init__(self):
        self.weights = None
        self.intercept = None

    def _add_bias(self, X: np.ndarray) -> np.ndarray:
        return np.c_[np.ones((X.shape[0], 1)), X]

    def fit_normal(self, X: np.ndarray, y: np.ndarray):
        X_b = self._add_bias(X)
        # Closed-form solution: theta = (X^T * X)^(-1) * X^T * y
        theta = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
        self.intercept = theta[0]
        self.weights = theta[1:]

    def fit_gd(self, X: np.ndarray, y: np.ndarray, alpha: float = 0.01, epochs: int = 1000):
        X_b = self._add_bias(X)
        m, n = X_b.shape
        theta = np.zeros(n)
        y = y.flatten()

        for _ in range(epochs):
            gradients = (2 / m) * X_b.T @ (X_b @ theta - y)
            theta -= alpha * gradients

        self.intercept = theta[0]
        self.weights = theta[1:]

    def predict(self, X: np.ndarray) -> np.ndarray:
        return X @ self.weights + self.intercept


# --- 3. Execution & Verification ---
if __name__ == "__main__":
    # Generate Data
    df = generate_smart_grid_dataset(n_samples=1200, random_seed=42)
    X = df[["Ambient_Temp_C", "Cluster_Utilization_Pct", "Chiller_Demand_kW", "Uptime_Hours"]].values
    y = df["Total_Power_kW"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 1. Scikit-Learn Model
    sklearn_model = LinearRegression()
    sklearn_model.fit(X_train, y_train)

    # 2. Custom Normal Equation Model
    custom_normal = CustomLinearRegression()
    custom_normal.fit_normal(X_train, y_train)

    # 3. Custom Gradient Descent Model (requires feature scaling)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    custom_gd = CustomLinearRegression()
    custom_gd.fit_gd(X_train_scaled, y_train, alpha=0.05, epochs=5000)

    # Display Coefficient Comparisons
    print(f"{'Parameter':<20} | {'Scikit-Learn':<15} | {'Custom Normal Eq.':<18}")
    print("-" * 60)
    print(f"{'Intercept':<20} | {sklearn_model.intercept_:<15.4f} | {custom_normal.intercept:<18.4f}")
    for i, name in enumerate(["X1 (Temp)", "X2 (Util)", "X3 (Chiller)", "X4 (Uptime)"]):
        print(f"{name:<20} | {sklearn_model.coef_[i]:<15.4f} | {custom_normal.weights[i]:<18.4f}")

    # Tolerance Check
    intercept_match = np.isclose(sklearn_model.intercept_, custom_normal.intercept, atol=1e-4)
    coef_match = np.allclose(sklearn_model.coef_, custom_normal.weights, atol=1e-4)

    print("\n--- Model Validation Result ---")
    print(f"Parameters match Scikit-Learn up to 4 decimal places: {intercept_match and coef_match}")

    # Evaluation Metrics
    y_pred = custom_normal.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Test MSE: {mse:.4f}")
    print(f"Test R² Score: {r2:.4f}")