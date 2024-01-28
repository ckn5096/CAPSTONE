from backend.app import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


# Profile relationship
profile = db.relationship('Profile', backref='user', lazy=True)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    bio = db.Column(db.Text)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class MusicPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_genres = db.Column(db.String(255))
    favorite_artists = db.Column(db.String(255))
    moods = db.Column(db.String(50))


user = db.relationship('User', backref=db.backref('music_preference', lazy=True))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.relationship('User', backref='playlists', lazy=True)
    songs = db.relationship('Song', secondary='playlist_song_association', backref='playlists', lazy=True)


playlist_song_association = db.Table('playlist_song_association',
                                     db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'),
                                               primary_key=True),
                                     db.Column('song_id', db.Integer, db.ForeignKey('song_id'), primary_key=True))
