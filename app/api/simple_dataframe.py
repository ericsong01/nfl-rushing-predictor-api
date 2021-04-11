import pandas as pd
import numpy as np
import app.data_models as data_models
from app.utils import Utils

class SimpleDataframe:

    df = None

    def __init__(self, data):
        team, yardline, player, direction = data[0], data[1], data[2], data[3]
        quarter, minutes, seconds = int(data[4]), int(data[5]), int(data[6])
        SEASON = 2020 

        X = Utils.standardize_x(yardline, direction.lower())
        std_yards = X 
        std_gameclock = Utils.convert_time_to_seconds(minutes, seconds)

        data = [team, X, player, std_yards, SEASON, quarter, std_gameclock]
        data_array = np.array(data)[np.newaxis, :]
        self.df = pd.DataFrame(data_array, columns=['Team', 'X', 'DisplayName','YardLine','Season','Quarter','GameClock'])

    def predict(self):
        self.df.iloc[:,[0,2]] = data_models.encoder.transform(self.df.iloc[:,[0,2]])
        pred_array = data_models.model.predict(self.df)
        y_pred = np.clip(np.cumsum(pred_array, axis=1), 0, 1).tolist()[0]
        
        return y_pred

        
        


"""
team = TEAM_FIELDS[form.team.data].lower()
        yardline = form.yardline.data 
        std_yards = standardize_x_yards(yardline, PLAY_DIR_FIELDS[form.direction.data])
        X = standardize_x_yards(yardline, PLAY_DIR_FIELDS[form.direction.data])
        player = form.myPlayer.data 
        season = 2020
        quarter = int(form.quarter.data) 
        minutes = int(form.gameclock_minutes.data)
        seconds = int(form.gameclock_seconds.data) 
        gameclock = convert_to_seconds(minutes ,seconds)

        print("Team:", TEAM_FIELDS[form.team.data])
        print("Yard Line:", form.yardline.data)
        print("Quarter:", form.quarter.data)
        print("Gameclock: %s:%s" % (form.gameclock_minutes.data, form.gameclock_seconds.data))
        print("Player: %s" % (form.myPlayer.data))
        print("Prediction Lower Bound: %s" % (form.low_yardage.data))
        print("Prediction Upper Bound: %s" % (form.high_yardage.data))
        data = [team, X, player, std_yards, season, quarter, gameclock]
        data_array = np.array(data)[np.newaxis, :]
        df = pd.DataFrame(data_array, columns=['Team', 'X', 'DisplayName','YardLine','Season','Quarter','GameClock'])
        print(df)

        # Perform encoding 
        df.iloc[:,[0,2]] = data_models.encoder.transform(df.iloc[:,[0,2]])
        print("After encode")
        # data_models.scaler.transform(df)
        print("After transform")
        array = data_models.model.predict(df)
        print("After predict")
        y_pred = np.clip(np.cumsum(array, axis=1), 0, 1).tolist()[0]

        print("Predictions:", y_pred)
"""
