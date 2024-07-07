from pathlib import Path

import pandas as pd
import pandas.testing as pd_testing
import pytest

from src.data_processing import process_data


def read_resource(filename):
    current_dir = Path(__file__).parent
    input_file = current_dir / "resources" / filename
    return pd.read_csv(input_file)


@pytest.fixture
def sample_data():
    return read_resource("input.csv")


@pytest.fixture
def expected_df():
    df = read_resource("expected_output.csv")
    df["departure_hour"] = df["departure_hour"].astype("int32")
    return df


def test_process_data(sample_data, expected_df):
    # Process the data
    processed_df = process_data(sample_data)

    # Expected columns after processing
    expected_columns = [
        "electric_bike",
        "departure_hour",
        "membership_cat_annual_pass",
        "membership_cat_other",
        "membership_cat_pay_per_ride",
        "membership_cat_community_pass",
        "membership_cat_unknown",
        "membership_cat_monthly_pass",
        "duration_min",
        "departure_temperature_c",
    ]

    assert all(
        col in processed_df.columns for col in expected_columns
    ), "Not all expected columns are in the processed DataFrame"

    for col in processed_df.columns:
        assert col in expected_columns, f"Unexpected column {col} found in processed DataFrame"

    assert all(processed_df["duration_min"] > 0), "Found values <= 0 in duration_min"
    assert all(processed_df["duration_min"] < 270), "Found values >= 270 in duration_min"

    assert len(processed_df) == 2, "The number of rows in the processed DataFrame is not as expected"
    pd_testing.assert_frame_equal(processed_df, expected_df)


# Run the tests
if __name__ == "__main__":
    pytest.main()
