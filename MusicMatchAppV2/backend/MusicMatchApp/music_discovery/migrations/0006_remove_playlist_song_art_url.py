# Generated by Django 4.2.9 on 2024-03-02 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("music_discovery", "0005_playlist_song_art_url"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="playlist",
            name="song_art_url",
        ),
    ]
