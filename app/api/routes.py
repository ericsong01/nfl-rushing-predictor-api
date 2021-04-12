from app.api import bp 
from flask import jsonify, request, Response
import json
from app.api.kaggle_dataframe import KaggleDataframe, DataframeException
from app.api.simple_dataframe import SimpleDataframe

"""Accepts a dataframe as a CSV file. Outputs JSON prediction info"""
@bp.route('/predict-kaggle-data', methods=['POST'])
def kaggle_prediction():
    csv_file = request.files["dataframe_csv"]
    
    try:
        kaggle_df = KaggleDataframe(csv_file)
        kaggle_df.clean_features()
        kaggle_df.standardize_features()
        kaggle_df.engineer_features()

        prediction = kaggle_df.get_prediction()
    except DataframeException as e:
        return str(e), 400
    except Exception:
        return "Unexpected data input formats", 400

    prettified_pred = prettify_prediction(prediction)
    return jsonify(prettified_pred)


"""Accepts form-data input and outputs prediction array"""
@bp.route('predict-simple', methods=['POST'])
def simple_prediction():
    try:
        
        # Retrieve a validate data 
        data = request.get_json(force=True)
        
        # Convert data into a pd dataframe and perform prediction
        simple_df = SimpleDataframe(data)
        prediction = simple_df.predict()

    except Exception as e:
        return str(e), 400

    prettified_pred = prettify_prediction(prediction)
    return jsonify(prettified_pred)
    

"""Prettify prediction array returned by df classes"""
def prettify_prediction(pred):
    labeled_predictions = []
    for i in range(len(pred)):
        labeled_predictions.append("Gain {} Yards: {}".format(i-99, pred[i]))
 
    return labeled_predictions


    