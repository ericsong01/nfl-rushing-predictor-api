from app.api import bp 
from flask import jsonify, request
import json
from app.api.kaggle_dataframe import KaggleDataframe
from app.api.simple_dataframe import SimpleDataframe

"""
Data Input Process:
1. From dataframe, convert to JSON using df.to_json(orient="table")
2. Pass JSON into POST request

"""

"""Accepts a dataframe as a CSV file (converted into csv with index=False)"""
@bp.route('/predict-kaggle-data', methods=['POST'])
def kaggle_prediction():
    csv_file = request.files["dataframe_csv"]
    
    try:
        kaggle_df = KaggleDataframe(csv_file)
    except Exception as e:
        return str(e)

    kaggle_df.clean_features()
    kaggle_df.standardize_features()
    kaggle_df.engineer_features()

    prediction = kaggle_df.get_prediction()

    prettified_pred = prettify_prediction(prediction)
    return jsonify(prettified_pred)

"""Accepts JSON input and outputs prediction array"""
@bp.route('predict-simple', methods=['POST'])
def simple_prediction():
    try:
        
        # Retrieve a validate data 
        data = request.get_json(force=True)
        data_list = validate_extract_fields(data)

        # Convert data into a pd dataframe and perform prediction
        simple_df = SimpleDataframe(data_list)
        prediction = simple_df.predict()

        prettified_pred = prettify_prediction(prediction)
        return jsonify(prettified_pred)
    
    # Handle user input errors 
    except KeyError as e:
        return str(e)
    except Exception as e:
        return str(e) 
    except TypeError as e:
        return str(e)

"""Prettify prediction array"""
def prettify_prediction(pred):
    labeled_predictions = []
    for i in range(len(pred)):
        labeled_predictions.append("Gain {} Yards: {}".format(i-99, pred[i]))
 
    return labeled_predictions

"""Validate inputs and return data as an array"""
def validate_extract_fields(data):
    try:
        valid_team_fields = ["home", "away"]
        team = data["team"]
        if team.lower() not in valid_team_fields:
            raise Exception("Invalid input: Team")

        yardline = int(data["yardline"])
        if yardline < 0 or yardline > 50:
            raise Exception("Invalid input: Yardline")

        direction = data["direction"]
        if direction.lower() not in ["right", "left"]:
            raise Exception("Invalid input: Direction")

        quarter = int(data["quarter"])
        if quarter < 1 or quarter > 4:
            raise Exception("Invalid input: Quarter")

        minutes = int(data["gameclock_minutes"])
        if minutes < 0 or minutes > 15:
            raise Exception("Invalid input: Gameclock minutes can only be in the interval [0,15]")

        seconds = int(data["gameclock_seconds"])
        if seconds < 0 or seconds > 59:
            raise Exception("Invalid input: Gameblock seconds can only be in the interval [0,59]")

        player = data["player_name"]

        data_list = [team, yardline, player, direction, quarter, minutes, seconds]
        return data_list

    except KeyError:
        raise KeyError("Invalid or missing form fields")

    except ValueError:
        raise ValueError("Invalid input type for numeric fields")

    