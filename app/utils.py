import app.data_models
import joblib 
import math

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

        print("Kaggle Model:", app.data_models.model)
        print("Kaggle Encoder:", app.data_models.encoder)

    @staticmethod
    def convert_gameclock_to_seconds(str):
        split_str = str.split(':')
        return int(split_str[0])*60 + int(split_str[1]) + int(split_str[2])/60

    @staticmethod
    def convert_time_to_seconds(minutes, seconds):
        return (minutes * 60) + seconds

    @staticmethod
    def to_inches(height):
        ft_inch = height.split('-')
        feet = int(ft_inch[0])
        inch = int(ft_inch[1])
        return (feet*12) + inch

    @staticmethod
    def yardLine(posTeam, fieldPosition, yardLine):
        # Still on own field side - we have to account for the endzone too
        if posTeam == fieldPosition: 
            return 10 + yardLine
        else: 
            return 60 + (50 - yardLine)

    @staticmethod
    def standardize_x(x, playDir):
        if playDir == 'left':
            return 120 - x
        else:
            return x

    @staticmethod
    def standardize_y(y, playDir):
        if playDir == 'left':
            return 53.3 - float(y)
        else:
            return y

    @staticmethod
    def standardize_orientation(ori, playDir):
        if playDir == 'left':
            return 180 + ori
        else:
            return ori

    @staticmethod
    def standardize_direction(direc, playDir):
        if playDir == 'left':
            return 180 + direc
        else:
            return direc

    @staticmethod
    def distance(rush_x, rush_y, def_x, def_y):
        return abs(math.sqrt(pow(def_x - rush_x, 2) + pow(def_y - rush_y, 2)))

    @staticmethod 
    def offense(df):
        personnel = df['OffensePersonnel']
        RB = 0
        TE = 0
        WR = 0
        OL = 0
        QB = 0
        prevChar = personnel[0]
        positions = ['OL','RB','TE','WR','LB']
        for i in range(len(personnel)): 
            symbol = prevChar + personnel[i]
            if symbol in positions:
                count = personnel[i-3]
                if (symbol == 'OL'):
                    OL = int(count)
                elif (symbol == 'RB'):
                    RB = int(count)
                elif (symbol == 'TE'):
                    TE = int(count)
                elif (symbol == 'WR'):
                    WR = int(count)
                elif (symbol == 'QB'):
                    QB = int(count)
            prevChar = personnel[i]
            
        # Default to 1 QB 
        if (QB == 0):
            QB = 1
        
        # Handle cases w/ strange offense personnel such as having a DB or LB which are defensive positions 
        # I'll assume those become an OL position 
        if (OL == 0) | (RB + TE + WR + OL + QB != 11):
            OL = 11 - RB - TE - WR - QB 
            
        df['RB'] = RB
        df['TE'] = TE
        df['WR'] = WR
        df['OL'] = OL
        df['QB'] = QB
        return df

    @staticmethod
    def defense(df):
        personnel = df['DefensePersonnel']
        DL = 0
        DB = 0
        LB = 0
        prevChar = personnel[0]
        positions = ['DL','DB','LB']
        for i in range(len(personnel)): 
            symbol = prevChar + personnel[i]
            if symbol in positions:
                count = personnel[i-3]
                if (symbol == 'DL'):
                    DL = int(count)
                elif (symbol == 'DB'):
                    DB = int(count)
                elif (symbol == 'LB'):
                    LB = int(count)
            prevChar = personnel[i]
            
        # Handle cases w/ strange defensive personnel such as having a RB or OL which are offensive positions 
        # I'll assume those take on DL positions 
        if (DL == 0) | (DL + DB + LB!= 11):
            OL = 11 - DB - LB
            
        df['DL'] = DL
        df['DB'] = DB
        df['LB'] = LB
        return df

    @staticmethod
    def line_diff(ol,te,dl,lb):
        return (ol + te) - (dl + lb)

    @staticmethod
    def get_year(handoff, birth):
        age = handoff.year - birth.year - ((handoff.year, handoff.day) < (birth.month, birth.day))
        return age

    @staticmethod 
    def distance_behind_line(x, yardLine):
        return yardLine - x

    @staticmethod 
    def distance_to_endzone(yardLine):
        return 110 - yardLine



    
     


