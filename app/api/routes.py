from app.api import bp 
from flask import jsonify, request
import json
from app.api.api_utils import KaggleDataframe

"""
Data Input Process:
1. From dataframe, convert to JSON using df.to_json(orient="table")
2. Pass JSON into POST request

"""

@bp.route('/predict-kaggle-data', methods=['POST'])
def prediction():
    data = request.get_json(force=True)
    data = str(data).replace("\'", "\"")
    json_res = json.loads(data)
    
    df = KaggleDataframe(json_res)
    df.validate_df()
    df.clean_features()
    df.standardize_features() 
    df.engineer_features()

    prediction = df.get_prediction()

    labeled_predictions = []
    for i in range(len(prediction)):
        labeled_predictions.append("Gain {} Yards: {}".format(i-99, prediction[i]))

    # Convert to df 
    return jsonify(labeled_predictions)