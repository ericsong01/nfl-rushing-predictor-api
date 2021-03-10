from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import InputRequired, EqualTo, NumberRange
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets

# TEAM_FIELDS = [('1','NE'), ('2','KC'), ('3','BUF'), ('4','NYJ'), ('5','ATL'), ('6','CHI'), 
#                 ('7','CIN'), ('8','BAL'), ('9','CLE'), ('10','PIT'), ('11','ARI'), ('12','DET'), 
#                 ('13','JAX'), ('14','HOU'), ('15','OAK'), ('16','TEN'), ('17','WAS'), ('18','PHI'), 
#                 ('19','LA'), ('20','IND'), ('21','SEA'), ('22','GB'), ('23','CAR'), ('24','SF'), ('25','DAL'), 
#                 ('26','NYG'), ('27','NO'), ('28','MIN'), ('29','DEN'),('30','LAC'), ('31','TB'), ('32','MIA')]
TEAM_FIELDS = [('1','Home'), ('2','Away')]
PLAY_DIR_FIELDS = [('1','Right'),('2','Left')]
QUARTER_FIELDS = [('1','1'),('2','2'),('3','3'),('4','4')]
class SimplePredictionForm(FlaskForm):
    team = SelectField(u'Team',choices=TEAM_FIELDS, validators=[InputRequired()])
    yardline = h5fields.IntegerField("Yard Line", widget=h5widgets.NumberInput(min=0, max=50, step=1),validators=[InputRequired(),NumberRange(min=0,max=59,message="Must be between 0 and 50")])
    direction = SelectField(u'Play Direction',choices=PLAY_DIR_FIELDS,validators=[InputRequired()])
    quarter = SelectField(u'Quarter',choices=QUARTER_FIELDS,validators=[InputRequired()])
    gameclock_minutes = h5fields.IntegerField("Minutes", widget=h5widgets.NumberInput(min=0, max=15, step=1),validators=[InputRequired(),NumberRange(min=0,max=59,message="Must be between 0 and 15")])
    gameclock_seconds = h5fields.IntegerField("Seconds", widget=h5widgets.NumberInput(min=0, max=59, step=1),validators=[InputRequired(),NumberRange(min=0,max=59,message="Must be between 0 and 59")])
    myPlayer = StringField('Player', validators=[InputRequired()])
    low_yardage = h5fields.IntegerField("Lower Bound", widget=h5widgets.NumberInput(min=-99, max=99, step=1),validators=[InputRequired(),NumberRange(min=-99,max=99,message="Must be between -99 and 99")])
    high_yardage = h5fields.IntegerField("Higher Bound", widget=h5widgets.NumberInput(min=-99, max=99, step=1),validators=[InputRequired(),NumberRange(min=-99,max=99,message="Must be between -99 and 99")])

