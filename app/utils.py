import app.data_models
import joblib 

class Utils:

    @staticmethod
    def load_model_and_utils():
        simple_model_filename = "data_models/nfl_model1.pkl"
        simple_encoder_filename = "data_models/nfl_encoder1.pkl"

        kaggle_model_filename = "data_models/nfl_model_kaggle.pkl"
        kaggle_encoder_filename = "data_models/nfl_encoder_kaggle.pkl"
        
        app.data_models.model = joblib.load(simple_model_filename)
        app.data_models.encoder = joblib.load(simple_encoder_filename)
        app.data_models.kaggle_encoder = joblib.load(kaggle_encoder_filename)
        app.data_models.kaggle_model = joblib.load(kaggle_model_filename)

        print("Kaggle Model:", app.data_models.kaggle_model)
        print("Kaggle Encoder:", app.data_models.kaggle_encoder)



    
     


