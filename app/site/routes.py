from app.site import bp 
from app.site.forms import RegisterForm, LoginForm, SimplePredictionForm
from flask import render_template, redirect, url_for, request
from werkzeug.urls import url_parse 
from app.models import User 
from app.extensions import db 
from flask_login import current_user, login_required, login_user, logout_user
import pickle, json
import pandas as pd 
import numpy as np 
import data_models

""" TODO:
1. Refactor the code
2. Test if the standard scaler actually does anything, if it does, refit it 
3. Configure the prediction to output the actual probability and not just create a list 
"""

TEAM_FIELDS = {'1':'Home','2':'Away'}
PLAY_DIR_FIELDS = {'1':'Right','2':'Left'}
QUARTER_FIELDS = {'1':'1','2':'2','3':'3','4':'4'}

@bp.route('/',methods=['POST','GET'])
@bp.route('/index',methods=['POST','GET'])
@login_required
def index():

    with open('app/namelist.pkl','rb') as pkl:
        player_list = pickle.load(pkl)
    form = SimplePredictionForm()

    if form.validate_on_submit():
        print(form.team.data, form.yardline.data, form.quarter.data, form.gameclock_minutes.data, form.gameclock_seconds.data, form.myPlayer.data)
        
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

        return render_template('index.html',form=form,player_list=json.dumps(player_list),prediction="This ia a prediction")

    # return render_template('index.html',form=form,player_list=player_list)
    return render_template('index.html',form=form,player_list=json.dumps(player_list))

def standardize_x_yards(yard, playDir):
    if playDir == 'Left':
        return 110 - int(yard)
    else:
        return yard + 10

def convert_to_seconds(minutes, seconds):
    return (minutes * 60) + seconds

@bp.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))
        
    if form.validate_on_submit():
        user = User(email=form.email.data,name=form.name.data)
        user.set_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('site.login'))

    return render_template('register.html', form=form)

@bp.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user is None) or not user.check_password(form.password.data):
            return redirect(url_for('site.login')) 

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        print(next_page)
        if not next_page or url_parse(next_page).netloc != '':
            print("success")
            return redirect(url_for('site.index'))
        return redirect(next_page)
    
    return render_template('login.html',form=form)
    
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.login'))
