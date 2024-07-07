import os
import pytest
from unittest.mock import patch
import pandas as pd
from src.cli import parse_s3_path, read_from_local, write_to_local, read_from_s3, write_to_s3
from src.utils import create_s3_client


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c']
    })

def test_parse_s3_path():
    s3_path = "s3://mybucket/myfolder/myfile.csv"
    bucket, key = parse_s3_path(s3_path)
    assert bucket == "mybucket"
    assert key == "myfolder/myfile.csv"

def test_read_from_local(tmp_path):
    file_path = tmp_path / "test.csv"
    df = pd.DataFrame({
        'column1': [1, 2, 3],
        'column2': ['a', 'b', 'c']
    })
    df.to_csv(file_path, index=False)
    read_df = read_from_local(file_path)
    pd.testing.assert_frame_equal(df, read_df)

def test_write_to_local(tmp_path, sample_df):
    file_path = tmp_path / "test.csv"
    write_to_local(sample_df, file_path)
    read_df = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(sample_df, read_df)

@patch.dict(os.environ, {'S3_ENDPOINT_URL': 'http://localhost:4566'})
def test_create_s3_client_with_endpoint():
    client = create_s3_client()
    assert client.meta.endpoint_url == 'http://localhost:4566'
