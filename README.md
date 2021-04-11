# nflrushingpredictor

## How to get Dataset
1. Download the training dataset (train.csv) from: https://www.kaggle.com/c/nfl-big-data-bowl-2020/data

### Running the dataset through the predictor 
1. Extract a single play from the dataset following the steps below: 
   1. Read in the entire dataset: `df = pd.read_csv('train.csv', low_memory=False)`  
   2. Extract any 22 rows that all share the same PlayID: To exract the 2nd play in the dataset use `single_play_df = df.iloc[22:44]`
   3. Write the new dataframe into a csv file: `single_play_df.to_csv("input.csv",index=False)`
2. Send a POST request to: URL
   1. Using form-data encoded body: 
      `key = dataframe_csv`   `value=input.csv`
