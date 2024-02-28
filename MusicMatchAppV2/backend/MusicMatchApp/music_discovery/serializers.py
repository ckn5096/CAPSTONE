from rest_framework import serializers
from .models import MusicPreference, Playlist


class MusicPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicPreference
        fields = ['favorite_genre', 'favorite_artist', 'favorite_song']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['name', 'tracks']