from src.lib import convert_to_int, map_membership_type, standardize_column_names, one_hot_encode
import pandas as pd


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process the input DataFrame by converting specified columns to integers,
    parsing datetime columns, performing one-hot encoding, and cleaning up the data.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    columns_to_convert = ['Bike', 'Covered distance (m)']

    df = convert_to_int(df, columns_to_convert)

    df['Departure'] = pd.to_datetime(df['Departure'], errors='coerce', format='%Y-%m-%d %H:%M')

    df['departure_day'] = df['Departure'].dt.date
    df['departure_hour'] = df['Departure'].dt.hour

    df['membership_cat'] = df['Membership type'].apply(map_membership_type)

    df = one_hot_encode(df, "membership_cat", [
        "membership_cat_Other", "membership_cat_Pay Per Ride", "membership_cat_Community Pass",
        "membership_cat_Monthly Pass", "membership_cat_Annual Pass", "membership_cat_Unknown"])

    boolean_columns = ["Electric bike"]
    df[boolean_columns] = df[boolean_columns].astype(int)

    # Convert duration from seconds to minutes and filter based on duration
    # 270 is 99.5 percentile of Apr 2024 data
    df["duration_min"] = (df["Duration (sec.)"] / 60).astype(int)
    df = df.query("duration_min > 0 and duration_min < 270")

    df = df.drop(["Departure", "Return", "Return station", "Return temperature (C)",
             "Number of stopovers", "Stopover duration (sec.)",
             "Membership type", "Covered distance (m)"], axis=1)

    # Drop additional columns for now, might use in future version
    df = df.drop(["Departure station", "departure_day", "Bike", "Duration (sec.)"], axis=1)

    df = standardize_column_names(df)

    return df

