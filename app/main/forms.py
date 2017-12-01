from flask_wtf import Form
from wtforms.fields import StringField, RadioField, SubmitField
from wtforms.validators import Required


# class IndexForm(Form):
#     """Selects a room or creates a new one."""
#     teams = RadioField('Select a side', choices = [('1','Team 1'), ('2','Team 2'),('0','Neutral')])
#     submit = SubmitField('Stream a new Match')

class CreateRoomForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Alias', validators=[Required()])
    side = RadioField('Select a side', choices = [('1','Manchester United'), ('2','Chelsea'),('0','Neutral')], validators=[Required()])
    submit = SubmitField('Next')

class StartStreamingForm(Form):
    submit = SubmitField('Next')

class JoinRoomForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    submit = SubmitField('Enter Chatroom')
