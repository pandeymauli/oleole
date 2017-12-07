from flask_wtf import Form
from wtforms.fields import StringField, RadioField, SubmitField
from wtforms.validators import Required


# class IndexForm(Form):
#     """Selects a room or creates a new one."""
#     teams = RadioField('Select a side', choices = [('1','Team 1'), ('2','Team 2'),('0','Neutral')])
#     submit = SubmitField('Stream a new Match')

class CreateRoomForm(Form):
    """Create a room for featured match."""
    name = StringField('Set an alias', validators=[Required()])
    #side = RadioField('Select a side', choices = [('1','Manchester United'), ('2','Chelsea'),('0','Neutral')], validators=[Required()])
    #side = RadioField('Select a side', choices = [])
    side = RadioField('Pick your side')
    submit = SubmitField('Kick Off!')

class StartStreamingForm(Form):
    submit = SubmitField('Kick Off!')

class JoinRoomForm(Form):
    """Accepts a nickname and a room link."""
    name = StringField('Set an alias', validators=[Required()])
    side = RadioField('Pick your side', choices = [('1','CFC'), ('2','Neutral'),('3','MUFC')], validators=[Required()])
    room = StringField('Enter room code', validators=[Required()])
    submit = SubmitField('Kick Off!')

class DropLinkForm(Form):
    """Accepts a YouTube URL and creates a room."""
    videoURL = StringField('Drop a YouTube link of any match you want to watch together', validators=[Required()])
    team1 = StringField('Team 1')
    team2 = StringField('Team 2')
    submit = SubmitField('Next')
