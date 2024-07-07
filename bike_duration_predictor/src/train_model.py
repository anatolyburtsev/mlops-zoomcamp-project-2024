from dataclasses import dataclass

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


@dataclass
class ModelMetrics:
    """A data class to store the evaluation metrics of a trained model.

    Attributes
    ----------
       mse (float): Mean Squared Error of the model.
       mae (float): Mean Absolute Error of the model.
       r2 (float): R-squared score of the model.

    """

    mse: float
    mae: float
    r2: float


@dataclass
class TrainedModel:
    """A data class to store the trained model and its evaluation metrics.

    Attributes
    ----------
        metrics (ModelMetrics): An instance of ModelMetrics containing the evaluation metrics of the model.
        model (LinearRegression): The trained Linear Regression model.

    """

    metrics: ModelMetrics
    model: LinearRegression


def train_model(df: pd.DataFrame, target_column="duration_min") -> TrainedModel:
    x = df.drop([target_column], axis=1)
    y = df[[target_column]]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    full_train_model = LinearRegression()
    full_train_model.fit(x, y)
    metrics = ModelMetrics(mse=mse, mae=mae, r2=r2)

    return TrainedModel(metrics=metrics, model=full_train_model)
