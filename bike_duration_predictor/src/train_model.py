import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from dataclasses import dataclass
from sklearn.linear_model import LinearRegression


@dataclass
class ModelMetrics:
    mse: float
    mae: float
    r2: float


@dataclass
class TrainedModel:
    metrics: ModelMetrics
    model: LinearRegression


def train_model(df: pd.DataFrame, target_column="duration_min") -> TrainedModel:
    X = df.drop([target_column], axis=1)
    y = df[[target_column]]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    full_train_model = LinearRegression()
    full_train_model.fit(X, y)
    metrics = ModelMetrics(mse=mse, mae=mae, r2=r2)

    return TrainedModel(metrics=metrics, model=full_train_model)
