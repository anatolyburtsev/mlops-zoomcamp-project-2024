import pandas as pd
import pytest

from src.lib import convert_to_int, map_membership_type, standardize_column_names


def test_convert_to_int():
    data = {"col1": ["1", "2.0", "three", "4"], "col2": ["5.0", "6", None, "eight"]}
    df = pd.DataFrame(data)

    columns_to_convert = ["col1", "col2"]

    result_df = convert_to_int(df, columns_to_convert)

    expected_data = {"col1": [1, 2], "col2": [5, 6]}
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df)


@pytest.mark.parametrize(
    "membership_type, expected",
    [
        ("365 Day Pass", "Annual Pass"),
        ("30 Day Pass", "Monthly Pass"),
        ("Community Pass Youth", "Community Pass"),
        ("Pay Per Ride", "Pay Per Ride"),
        ("VIP", "Other"),
        (None, "Unknown"),
        ("Unknown Pass", "Other"),
    ],
)
def test_map_membership_type(membership_type, expected):
    assert map_membership_type(membership_type) == expected


def test_standardize_column_names():
    # Prepare the test DataFrame
    data = {
        "Departure temperature (C)": [22, 23, 24],
        "Membership type": ["365 Day Pass", "30 Day Pass", "Community Pass"],
        "Electric bike": [True, False, True],
    }
    df = pd.DataFrame(data)

    # Apply the function
    result_df = standardize_column_names(df)

    # Expected DataFrame after standardizing column names
    expected_columns = ["departure_temperature_c", "membership_type", "electric_bike"]

    # Check if the column names match the expected column names
    assert list(result_df.columns) == expected_columns


# Run the tests
if __name__ == "__main__":
    pytest.main()
