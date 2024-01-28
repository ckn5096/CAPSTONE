from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.app import db, app

from .models import Profile, RegistrationForm, User, MusicPreference, Playlist, Song
from .forms import MusicPreferenceForm, PlaylistForm, SongForm


# Remove the second import statement for 'app'

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/music_preferences", methods=['GET', 'POST'])
@login_required
def music_preferences():
    form = MusicPreferenceForm()
    if form.validate_on_submit():
        music_preference = MusicPreference(
            user=current_user,
            favorite_genres=form.favorite_genres.data,
            favorite_artists=form.favorite_artists.data,
            mood=form.mood.data
        )
        db.session.add(music_preference)
        db.session.commit()
        flash('Music Preferences updated!', 'success')
        return redirect(url_for('music_preferences'))
    return render_template('music_preferences.html', form=form)


@app.route("/create_playlist", methods=['GET', 'POST'])
@login_required
def create_playlist():
    form = PlaylistForm()
    if form.validate_on_submit():
        playlist = Playlist(
            name=form.name.data,
            description=form.description.data,
            user=current_user
        )
        db.session.add(playlist)
        db.session.commit()
        flash('Playlist created successfully!', 'success')
        return redirect(url_for('home'))
    return


render_template('create_playlist.html', form=form)


@app.route("/edit_playlist/<int:playlist_id>", methods=['GET', 'POST'])
@login_required
def edit_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    form = PlaylistForm()

    if form.validate_on_submit():
        playlist.name = form.name.data
        playlist.description = form.description.data
        db.session.commit()
        flash('Playlist updated successfully!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.name.data = playlist.name
        form.description.data = playlist.description
        return
    render_template('edit_playlist.html', form=form)


@app.route("/delete_playlist/<int:playlist_id>", methods=['POST'])
@login_required
def delete_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    db.session.delete(playlist)
    db.session.commit()
    flash('Playlist deleted successfully!', 'success')
    return redirect(url_for('home'))


@app.route("/manage_songs/<int:playlist_id>", methods=['GET', 'POST'])
@login_required
def manage_songs(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    form = SongForm()

    if form.validate_on_submit():
        song = Song(
            title=form.title.data,
            artist=form.artist.data,
            playlist=playlist
        )
        db.session.add(song)
        db.session.commit()
        flash('Song added to playlist!', 'success')
        return
    redirect(url_for('manage_songs', playlist_id=playlist_id))
    return


render_template('manage_songs.html', playlist=playlist, form=form)
