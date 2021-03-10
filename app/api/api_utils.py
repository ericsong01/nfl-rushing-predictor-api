import pandas as pd
import numpy as np
import app.data_models as data_models
import math 

class KaggleDataframe:

    df = None # raw df to be manipulated
    model_df = None # df to be fed into model 

    def validate_df(self):
        
        if self.df["PlayId"].nunique() != 1: # Ensure only one play is passed through 
            return False

        required_cols = ['PlayId','Team','X','Y','S','A','Dis','Orientation','Dir','NflId',
        'DisplayName','JerseyNumber','Season','YardLine','Quarter','GameClock','PossessionTeam',
        'Down','Distance','FieldPosition','HomeScoreBeforePlay','VisitorScoreBeforePlay',
        'NflIdRusher','OffenseFormation','OffensePersonnel','DefendersInTheBox','DefensePersonnel',
        'TimeHandoff','TimeSnap','PlayerHeight','PlayerWeight','PlayerBirthDate',
        'HomeTeamAbbr','Week','StadiumType','Turf','GameWeather','Temperature']

        if set(required_cols).issubset(self.df.columns):
            return True 
        else:
            return False

    def __init__(self, json):
        # TODO: See if this is converting it to a pandas dataframe 
        self.df = pd.DataFrame.from_dict(json, orient="index")
        if not self.validate_df:
            raise Exception("Dataframe can't be initialized due to missing feature column")

    def clean_features(self):
        self.df.FieldPosition = self.df.FieldPosition.fillna('Neutral')
        self.df = self.df.fillna(method='ffill').fillna(method='bfill')

        self.df["StadiumType"] = self.df["StadiumType"].replace(['Outdoor', 'Open','Outddors', 'Oudoor','Ourdoor', 'Heinz Field','Outdor', 'Cloudy', 'Bowl', 'Outside', 'Retractable Roof', 'Indoor, Open Roof', 'Outdoor Retr Roof-Open','Retr. Roof - Open', 'Domed, Open', 'Domed, open', 'Indoor, roof open', 'OUTDOOR', 'Retr. Roof-Open'], 'Outdoors')
        self.df["StadiumType"] = self.df["StadiumType"].replace(['Indoor', 'Dome','Domed, closed', 'Closed Dome','Retr. Roof-Closed', 'Retr. Roof - Closed', 'Indoor, Roof Closed', 'Retr. Roof Closed', 'Domed', 'Outside','Retractable Roof - Closed', 'Dome, closed', 'indoor'], 'Indoors')

        self.df['Turf'] = self.df['Turf'].replace(['Field Turf', 'A-Turf Titan', 'UBU Sports Speed S5-M', 'DD GrassMaster', 
        'UBU Speed Series-S5-M', 'FieldTurf', 'FieldTurf 360', 'Artifical', 'FieldTurf360', 'Field turf',
    'Twenty Four/Seven Turf','SISGrass', 'Twenty-Four/Seven Turf', 'UBU-Speed Series-S5-M', 'Turf'], 'Artificial')
        self.df['Turf'] = self.df['Turf'].replace(['Grass', 'Natural Grass', 'Natural grass', 'grass', 'Naturall Grass', 'natural grass'], 'Natural')

        self.df['GameWeather'] = self.df['GameWeather'].replace(['Clear and warm','Sun & clouds','Sunny','Mostly Sunny',
                        'Clear','Mostly Cloudy','Mostly Coudy','Partly sunny', 'Partly Cloudy', 'Cloudy',
                        'Sunny, highs to upper 80s','Partly cloudy','Partly Sunny', '30% Chance of Rain',
                        'Cloudy, fog started developing in 2nd quarter','Coudy','Clear skies', 'cloudy', 'Fair', 'Mostly cloudy',
                       'Cloudy, chance of rain','Party Cloudy','Hazy','Cloudy and Cool', 'Rain Chance 40%', 'Clear and sunny', 'Mostly sunny',
                       'Sunny and warm', 'Partly clear', 'Cloudy, 50% change of rain','Clear and Sunny', 'Sunny, Windy', 'Clear and Cool',
                        'Sunny and clear', 'Mostly Sunny Skies', 'Partly Clouidy','Clear Skies', 'Sunny Skies', 'Overcast',
                           'T: 51; H: 55; W: NW 10 mph','Clear and cold','Partly cloudy and mild','Breezy','partly cloudy',
                                                        'Mostly Clear','sUNNY','overcast','Mostly clear','Mostly Sunny'],'Clear')
        self.df['GameWeather'] = self.df['GameWeather'].replace(['Controlled Climate', 'Indoors', 'N/A (Indoors)',
                                    'N/A Indoor','Indoor','N/A Indoors'],'Indoors')
        self.df['GameWeather'] = self.df['GameWeather'].replace(['Light Rain','Showers',
                                'Cloudy with periods of rain, thunder possible. Winds shifting to WNW, 10-20 mph.',
                                'Rain likely, temps in low 40s.','Scattered Showers', 'Cloudy, Rain', 'Rain shower',
                                    'Rainy','Light rain','Cloudy with showers and wind','Raining', 'Rain and Wind'],'Rain')
        self.df['GameWeather'] = self.df['GameWeather'].replace(['Heavy lake effect snow', 'Cloudy, light snow accumulating 1-3"'],'Snow')
        self.df['GameWeather'] = self.df['GameWeather'].replace(['Cloudy and cold','Sunny and cold'],'Cold')

        self.df['PossessionTeam'] = self.df['PossessionTeam'].replace('BLT','BAL')
        self.df['PossessionTeam'] = self.df['PossessionTeam'].replace('CLV','CLE')
        self.df['PossessionTeam'] = self.df['PossessionTeam'].replace('ARZ','ARI')
        self.df['PossessionTeam'] = self.df['PossessionTeam'].replace('HST','HOU')

        self.df['FieldPosition'] = self.df['FieldPosition'].replace('BLT','BAL')
        self.df['FieldPosition'] = self.df['FieldPosition'].replace('CLV','CLE')
        self.df['FieldPosition'] = self.df['FieldPosition'].replace('ARZ','ARI')
        self.df['FieldPosition'] = self.df['FieldPosition'].replace('HST','HOU')

        self.df['DefendersInTheBox'] = pd.to_numeric(self.df["DefendersInTheBox"],errors='coerce')
        self.df['PlayerBirthDate'] = pd.to_datetime(self.df["PlayerBirthDate"], format='%m\/%d\/%Y', errors='coerce')
        self.df['TimeHandoff'] = pd.to_datetime(self.df['TimeHandoff'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')
        self.df['TimeSnap'] = pd.to_datetime(self.df['TimeSnap'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')

    def standardize_features(self):
        self.df['GameClock'] = self.df['GameClock'].apply(lambda x: LambdaFuncs.convert_gameclock_to_seconds(x))
        self.df['PlayerHeight'] = self.df['PlayerHeight'].apply(lambda x: LambdaFuncs.to_inches(x))
        self.df['YardLine'] = self.df[['PossessionTeam','FieldPosition','YardLine']].apply(lambda x: LambdaFuncs.yardLine(x[0],x[1],x[2]), axis=1)
        self.df["X"] = self.df[['X','PlayDirection']].apply(lambda x: LambdaFuncs.standardize_x(x[0],x[1]), axis=1)
        self.df["Y"] = self.df[['Y','PlayDirection']].apply(lambda y: LambdaFuncs.standardize_y(y[0],y[1]), axis=1)
        self.df["Orientation"] = self.df[['Orientation','PlayDirection']].apply(lambda x: LambdaFuncs.standardize_orientation(x[0],x[1]), axis=1)
        self.df["Dir"] = self.df[['Dir','PlayDirection']].apply(lambda x: LambdaFuncs.standardize_direction(x[0],x[1]), axis=1)

        self.df = self.df.drop(['Humidity','WindSpeed','WindDirection','Location','Stadium','PlayerCollegeName','PlayDirection','Position'], axis=1)

    def create_defensive_features(self, df):
        # Pull rusher specific values into a temporary df 
        rusher_df = df[df['NflId'] == df['NflIdRusher']][['GameId','PlayId','Team','X','Y']]
        rusher_df.columns = ['GameId','PlayId','RusherTeam','RusherX','RusherY']

        # Get only rows corresponding to the defensive team, but include rusher specific values 
        defense_df = pd.merge(df,rusher_df,on=['GameId','PlayId'],how='inner')
        defense_df = defense_df[defense_df['Team'] != defense_df['RusherTeam']]
        
        # Calculate distance from each defensive player to the rusher 
        defense_df['DistanceFromRusher'] = defense_df[['RusherX','RusherY','X','Y']].apply(lambda x: LambdaFuncs.distance(x[0],x[1],x[2],x[3]), axis=1)
        defense_df = defense_df[['GameId','PlayId','DistanceFromRusher']]
        
        # Collect min, max, mean, and std of distance from defensive players to the rusher for each play 
        defense_df = defense_df.groupby(['GameId','PlayId']).agg({'DistanceFromRusher':['min','max','mean','std']}).reset_index()
        defense_df.columns = ['GameId','PlayId','Def_min_dis_to_rusher','Def_max_dis_to_rusher','Def_mean_dis_to_rusher','Def_std_dis_to_rusher']
        return defense_df

    def engineer_features(self):
        train_df = self.df[self.df['NflId'] == self.df['NflIdRusher']]
        defense_df = self.create_defensive_features(self.df)
        train_df = pd.merge(train_df, defense_df, on=['GameId','PlayId'], how='inner')
        train_df = train_df.apply(LambdaFuncs.offense, axis=1)
        train_df = train_df.apply(LambdaFuncs.defense, axis=1)
        train_df = train_df.drop(['DefensePersonnel','OffensePersonnel'],axis=1)
        train_df['TacklerBlockerDifference'] = train_df[['OL','TE','DL','LB']].apply(lambda x: LambdaFuncs.line_diff(x[0],x[1],x[2],x[3]), axis=1)
        train_df['Age'] = train_df[['TimeHandoff','PlayerBirthDate']].apply(lambda x: LambdaFuncs.get_year(x[0],x[1]), axis=1)
        train_df = train_df.drop(['TimeHandoff','PlayerBirthDate','TimeSnap'], axis=1)
        train_df['DistanceBehindLine'] = train_df[['X','YardLine']].apply(lambda x: LambdaFuncs.distance_behind_line(x[0],x[1]),axis=1)
        train_df['DistanceToEndzone'] = train_df[['YardLine']].apply(lambda x: LambdaFuncs.distance_to_endzone(x[0]), axis=1)
        self.model_df = train_df

    def get_prediction(self):
        cat_features = ['Team', 'DisplayName', 'PossessionTeam', 'FieldPosition', 
                'HomeTeamAbbr', 'VisitorTeamAbbr', 'StadiumType',
               'Turf', 'GameWeather', 'OffenseFormation']
        self.model_df.drop(["GameId","PlayId","Yards"], axis=1, inplace=True)  
        self.model_df[cat_features] = data_models.kaggle_encoder.transform(self.model_df[cat_features])
        array = data_models.kaggle_model.predict(self.model_df) 
        return np.clip(np.cumsum(array, axis=1), 0, 1).tolist()[0]
    
    def __repr__(self):
        return self.df

class LambdaFuncs:

    @staticmethod
    def convert_gameclock_to_seconds(str):
        split_str = str.split(':')
        return int(split_str[0])*60 + int(split_str[1]) + int(split_str[2])/60

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
