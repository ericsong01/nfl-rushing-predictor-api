from app.api import bp 
from flask import jsonify, request
import json
from app.api.dataframes import KaggleDataframe

"""
Data Input Process:
1. From dataframe, convert to JSON using df.to_json(orient="table")
2. Pass JSON into POST request

"""

# Accepts a dataframe as a CSV file (converted into csv with index=False)
@bp.route('/predict-kaggle-data', methods=['POST'])
def prediction():
    csv_file = request.files["dataframe_csv"]
    
    try:
        kaggle_df = KaggleDataframe(csv_file)
    except Exception as e:
        return str(e)

    kaggle_df.clean_features()
    kaggle_df.standardize_features()
    kaggle_df.engineer_features()

    prediction = kaggle_df.get_prediction()

    labeled_predictions = []
    for i in range(len(prediction)):
        labeled_predictions.append("Gain {} Yards: {}".format(i-99, prediction[i]))
 
    return jsonify(labeled_predictions)
