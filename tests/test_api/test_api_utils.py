import pytest
import pandas as pd 

from app.api.api_utils import KaggleDataframe

# Run using `PYTHONPATH=. pytest`

class TestApiUtils:

    """

    Test validation of dataset: 
    1. JSON w/ Correct rows  

    """

    def test_KaggleDataframe_initialization_1(self):
        test_df = pd.read_csv('tests/test_api/api_test.csv',index_col=0, low_memory=False)
        
        error_message = "Dataframe can't be initialized due to missing feature column"
        with pytest.raises(Exception) as error_message:
            kaggle_df = KaggleDataframe(test_df,json=False)

