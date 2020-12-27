import joblib
import app.data_models

def load_model():
    model_filename = "data_models/nfl_model1.pkl"
    scaler_filename = "data_models/nfl_scaler1.pkl"
    encoder_filename = "data_models/nfl_encoder1.pkl"
    
    app.data_models.model = joblib.load(model_filename)
    app.data_models.scaler = joblib.load(scaler_filename)
    app.data_models.encoder = joblib.load(encoder_filename)
    
    print("Model:", app.data_models.model)
    print("Encoder:", app.data_models.encoder)
    print("Scaler:", app.data_models.scaler)