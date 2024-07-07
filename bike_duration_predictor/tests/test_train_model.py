import pytest
from sklearn.base import BaseEstimator

from src.train_model import TrainedModel, train_model
from tests.test_data_processing import read_resource


@pytest.fixture
def sample_df():
    return read_resource("train_model_input.csv")


def test_train_model(sample_df):
    trained_model = train_model(sample_df)

    assert isinstance(trained_model, TrainedModel)

    assert 0 <= trained_model.metrics.mse <= 1000
    assert 0 <= trained_model.metrics.mae <= 30
    assert -1 <= trained_model.metrics.r2 <= 1

    assert hasattr(trained_model, "model")
    assert isinstance(trained_model.model, BaseEstimator)
