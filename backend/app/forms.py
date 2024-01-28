from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MusicPreferenceForm(FlaskForm):
    favorite_genres = SelectMultipleField('Favorite Genres', validators=[DataRequired()],
                                          choices=[('pop', 'Pop'), ('rock', 'Rock'), ('hiphop', 'Hip Hop'),
                                                   ('jazz', 'Jazz'), ('classical', 'Classical'), ('house', 'House'),
                                                   ('alternative', 'Alternative'), ('latin', 'Latin')])
    favorite_artists = StringField('Favorite Artists', validators=[DataRequired()])
    mood = SelectField('Mood', validators=[DataRequired()],
                       choices=[('happy', 'Happy'), ('calm', 'Calm'), ('energetic', 'Energetic'), ('sad', 'Sad'),
                                ('angry', 'Angry')])


class PlaylistForm(FlaskForm):
    name = StringField('Playlist Name', validators=[DataRequired])
    description = TextAreaField('Description')
    submit = SubmitField('Create Playlist')


class SongForm(FlaskForm):
    title = StringField('Song Title', validators=[DataRequired])
    artist = StringField('Artist', validators=[DataRequired])
    submit = SubmitField('Add Song')
