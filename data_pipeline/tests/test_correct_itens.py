from unittest.mock import mock_open, patch
import pytest
import re
from utils._correct_itens import CorrectItem
from unittest.mock import patch
import pandas as pd

def test_correct_item_initialization():
    param_path = {"item": "path/to/files/*"}
    item = CorrectItem(param_path)
    assert item.param_path == param_path
    assert isinstance(item.uuid_pattern, re.Pattern)

def test_split_rows():
    item = CorrectItem({"item": "mock_path"})
    
    rows = [
        "123e4567-e89b-12d3-a456-426614174000,www.example.com,2023-01-01,2023-01-02,Some news content"
    ]
    
    result = item._split_rows(rows)
    
    assert result[0][0] == "123e4567-e89b-12d3-a456-426614174000"
    assert result[0][1] == "www.example.com"
    assert result[0][2] == "2023-01-01"
    assert result[0][3] == "2023-01-02"
    assert result[0][4] == "Some news content"


def test_list_to_df():
    item = CorrectItem({"item": "mock_path"})
    
    data = [
        ["123e4567-e89b-12d3-a456-426614174000", "www.example.com", "2023-01-01", "2023-01-02", "Some news content"]
    ]
    
    result_df = item._list_to_df(data)
    
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.shape == (1, 5)
    assert result_df.columns.tolist() == ["history", "page_url", "issued", "modified", "news_concat"]
    assert result_df["history"].iloc[0] == "123e4567-e89b-12d3-a456-426614174000"


def test_save_new_csv():
    item = CorrectItem({"item": "mock_path"})
    mock_df = pd.DataFrame([["123e4567-e89b-12d3-a456-426614174000", "www.example.com", "2023-01-01", "2023-01-02", "Some news content"]], 
                           columns=["history", "page_url", "issued", "modified", "news_concat"])
    
    with patch.object(mock_df, 'to_csv') as mock_to_csv:
        item._save_new_csv(mock_df, 1)
        mock_to_csv.assert_called_once_with("./source_files/correct_itens/cleaned_file_1.csv", 
                                            index=False, encoding="utf-8", escapechar="\\")

def test_uuid_clean_lines():
    mock_file = "123e4567-e89b-12d3-a456-426614174000\nSome other line\n123e4567-e89b-12d3-a456-426614174001"

    item = CorrectItem({"item": "mock_path"})

    with patch("builtins.open", mock_open(read_data=mock_file)):
        result = item._uuid_clean_lines("mock_path")

    assert len(result) >= 1
    assert "123e4567-e89b-12d3-a456-426614174001" in result[0]
