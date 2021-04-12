import pandas as pd
import numpy as np
import app.data_models as data_models
from app.utils import Utils

class SimpleDataframe:

    df = None

    def __init__(self, data):

        try:
            valid_data = self.validate_data(data)
        except Exception as e:
            raise Exception(e)
            
        # Extract data fields from valid_data array
        team, yardline, player, direction = valid_data[0], valid_data[1], valid_data[2], valid_data[3]
        quarter, minutes, seconds = valid_data[4], valid_data[5], valid_data[6]
        SEASON = 2020   
        
        # Standardize data before converting into pd dataframe
        X = Utils.standardize_x(yardline, direction.lower())
        std_yards = X 
        std_gameclock = Utils.convert_time_to_seconds(minutes, seconds)

        std_data = [team, X, player, std_yards, SEASON, quarter, std_gameclock]
        data_array = np.array(std_data)[np.newaxis, :]
        self.df = pd.DataFrame(data_array, columns=['Team', 'X', 'DisplayName','YardLine','Season','Quarter','GameClock'])

    def predict(self):
        self.df.iloc[:,[0,2]] = data_models.encoder.transform(self.df.iloc[:,[0,2]])
        pred_array = data_models.model.predict(self.df)
        y_pred = np.clip(np.cumsum(pred_array, axis=1), 0, 1).tolist()[0]
        
        return y_pred
    
    """Ensure data fields contain valid inputs and return an array w/ valid data fields"""
    def validate_data(self, data):
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

