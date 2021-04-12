import pandas as pd
import numpy as np
import app.data_models as data_models
from app.utils import Utils 

class DataframeException(Exception):
    """Exception to indicate issue w/ dataframe"""
    pass

class KaggleDataframe:

    df = None # raw df to be manipulated
    model_df = None # df to be fed into model 

    def __init__(self, csv):
        raw_df = pd.read_csv(csv)

        valid, error = self.validate_df(raw_df)

        if not valid:
            raise DataframeException(error)

        self.df = raw_df 
    
    def validate_df(self, df):
        
        # Ensure only one play data is contained in the dataframe
        if df["PlayId"].nunique() != 1: 
            error_message = "Only one play data is allowed (All PlayIDs must be identical)"
            return False, error_message
        
        # Ensure index col is formatted correct 
        if df.columns[0] == "Unnamed: 0":
            error_message = "When transforming the dataframe into a csv to pass into the POST request, ensure indexes aren't included"
            return False, error_message

        # Ensure all original data fields are included
        required_cols = ['PlayId','Team','X','Y','S','A','Dis','Orientation','Dir','NflId',
        'DisplayName','JerseyNumber','Season','YardLine','Quarter','GameClock','PossessionTeam',
        'Down','Distance','FieldPosition','HomeScoreBeforePlay','VisitorScoreBeforePlay',
        'NflIdRusher','OffenseFormation','OffensePersonnel','DefendersInTheBox','DefensePersonnel',
        'TimeHandoff','TimeSnap','PlayerHeight','PlayerWeight','PlayerBirthDate',
        'HomeTeamAbbr','Week','StadiumType','Turf','GameWeather','Temperature']
        if set(required_cols).issubset(df.columns):
            return True, ""
        else:
            error_message = "Ensure all original data fields from the Kaggle dataset are included"
            return False, error_message

    """Functions for cleaning + standardizing + engineering new features
        See nflbigdata repo for more """
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
        self.df['PlayerBirthDate'] = pd.to_datetime(self.df["PlayerBirthDate"], format='%m/%d/%Y', errors='coerce')
        self.df['TimeHandoff'] = pd.to_datetime(self.df['TimeHandoff'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')
        self.df['TimeSnap'] = pd.to_datetime(self.df['TimeSnap'], format='%Y-%m-%dT%H:%M:%S.%fZ', errors='coerce')

    def standardize_features(self):
        self.df['GameClock'] = self.df['GameClock'].apply(lambda x: Utils.convert_gameclock_to_seconds(x))
        self.df['PlayerHeight'] = self.df['PlayerHeight'].apply(lambda x: Utils.to_inches(x))
        self.df['YardLine'] = self.df[['PossessionTeam','FieldPosition','YardLine']].apply(lambda x: Utils.yardLine(x[0],x[1],x[2]), axis=1)
        self.df["X"] = self.df[['X','PlayDirection']].apply(lambda x: Utils.standardize_x(x[0],x[1]), axis=1)
        self.df["Y"] = self.df[['Y','PlayDirection']].apply(lambda y: Utils.standardize_y(y[0],y[1]), axis=1)
        self.df["Orientation"] = self.df[['Orientation','PlayDirection']].apply(lambda x: Utils.standardize_orientation(x[0],x[1]), axis=1)
        self.df["Dir"] = self.df[['Dir','PlayDirection']].apply(lambda x: Utils.standardize_direction(x[0],x[1]), axis=1)

        self.df = self.df.drop(['Humidity','WindSpeed','WindDirection','Location','Stadium','PlayerCollegeName','PlayDirection','Position'], axis=1)

    def create_defensive_features(self, df):
        rusher_df = df[df['NflId'] == df['NflIdRusher']][['GameId','PlayId','Team','X','Y']]
        rusher_df.columns = ['GameId','PlayId','RusherTeam','RusherX','RusherY']

        defense_df = pd.merge(df,rusher_df,on=['GameId','PlayId'],how='inner')
        defense_df = defense_df[defense_df['Team'] != defense_df['RusherTeam']]
        
        defense_df['DistanceFromRusher'] = defense_df[['RusherX','RusherY','X','Y']].apply(lambda x: Utils.distance(x[0],x[1],x[2],x[3]), axis=1)
        defense_df = defense_df[['GameId','PlayId','DistanceFromRusher']]
        
        defense_df = defense_df.groupby(['GameId','PlayId']).agg({'DistanceFromRusher':['min','max','mean','std']}).reset_index()
        defense_df.columns = ['GameId','PlayId','Def_min_dis_to_rusher','Def_max_dis_to_rusher','Def_mean_dis_to_rusher','Def_std_dis_to_rusher']
        return defense_df

    def engineer_features(self):
        train_df = self.df[self.df['NflId'] == self.df['NflIdRusher']]
        defense_df = self.create_defensive_features(self.df)
        train_df = pd.merge(train_df, defense_df, on=['GameId','PlayId'], how='inner')
        train_df = train_df.apply(Utils.offense, axis=1)
        train_df = train_df.apply(Utils.defense, axis=1)
        train_df = train_df.drop(['DefensePersonnel','OffensePersonnel'],axis=1)
        train_df['TacklerBlockerDifference'] = train_df[['OL','TE','DL','LB']].apply(lambda x: Utils.line_diff(x[0],x[1],x[2],x[3]), axis=1)
        train_df['Age'] = train_df[['TimeHandoff','PlayerBirthDate']].apply(lambda x: Utils.get_year(x[0],x[1]), axis=1)
        train_df = train_df.drop(['TimeHandoff','PlayerBirthDate','TimeSnap'], axis=1)
        train_df['DistanceBehindLine'] = train_df[['X','YardLine']].apply(lambda x: Utils.distance_behind_line(x[0],x[1]),axis=1)
        train_df['DistanceToEndzone'] = train_df[['YardLine']].apply(lambda x: Utils.distance_to_endzone(x[0]), axis=1)
        self.model_df = train_df

    def get_prediction(self):
        cat_features = ['Team', 'DisplayName', 'PossessionTeam', 'FieldPosition', 
                'HomeTeamAbbr', 'VisitorTeamAbbr', 'StadiumType',
               'Turf', 'GameWeather', 'OffenseFormation']
        self.model_df.drop(["GameId","PlayId","Yards"], axis=1, inplace=True)  
        self.model_df[cat_features] = data_models.kaggle_encoder.transform(self.model_df[cat_features])
        array = data_models.kaggle_model.predict(self.model_df) 
        return np.clip(np.cumsum(array, axis=1), 0, 1).tolist()[0]
    

