from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MusicPreference, Playlist
from .serializers import MusicPreferenceSerializer, PlaylistSerializer
from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


class IsTokenAuthenticated(BasePermission):
    """
    Custom permission to authenticate users using token from local storage.
    """

    def has_permission(self, request, view):
        token_key = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        try:
            token = Token.objects.get(key=token_key)
            request.user = token.user
            return True
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token is invalid or expired')


class MusicPreferenceView(APIView):
    permission_classes = [IsTokenAuthenticated]
    authentication_classes = [TokenAuthentication]

    # def get(self, request):
    #     try:
    #         # Get the music preference for the authenticated user
    #         music_preference = MusicPreference.objects.get(user=request.user)
    #         serializer = MusicPreferenceSerializer(music_preference)
    #         return Response(serializer.data)
    #     except MusicPreference.DoesNotExist:
    #         return Response({'message': 'No music preference set for this user'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        try:
            # Attempt to retrieve the music preference for the authenticated user
            music_preference = MusicPreference.objects.get(user=request.user)
            serializer = MusicPreferenceSerializer(music_preference)
            return Response(serializer.data)
        except MusicPreference.DoesNotExist:
            # If the preference does not exist, return a default null value
            return Response({'message': 'No music preference set for this user', 'music_preference': None},
                            status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MusicPreferenceSerializer(data=request.data)
        if serializer.is_valid():
            # Associate the music preference with the authenticated user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        music_preference = MusicPreference.objects.get(user=request.user)
        serializer = MusicPreferenceSerializer(music_preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        music_preference = MusicPreference.objects.get(user=request.user)
        music_preference.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class GeneratePlaylistView(APIView):
    permission_classes = [IsTokenAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        preferences = request.data

        # Get the user associated with the token
        token_key = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
        except Token.DoesNotExist:
            raise AuthenticationFailed('Token is invalid or expired')

        # Initialize Spotipy client with your Spotify Developer API credentials
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(client_id='71b57beac4374097b7fa168d2f2403bd',
                                                                client_secret='917821889f14406db3ecc8427ab7ac67'))

        # Get Spotify ID for the favorite artist
        artist_name = preferences.get('favorite_artist', '')
        if artist_name:
            # Search for the artist
            results = sp.search(q=artist_name, type='artist')
            artists = results['artists']['items']
            if artists:
                # Get the Spotify ID of the first artist in the search results
                favorite_artist_id = artists[0]['id']
            else:
                # Handle case where no artist is found
                return Response({'error': 'Favorite artist not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle case where favorite_artist is missing
            return Response({'error': 'Favorite artist is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Use user's preferences to generate recommended tracks
        recommended_tracks = sp.recommendations(seed_artists=[favorite_artist_id], limit=10)

        # Extract relevant information from recommended tracks
        recommended_songs = [{
            'name': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'album': track['album']['name'],
            'uri': track['uri']
        } for track in recommended_tracks['tracks']]

        # Save the generated playlist to the database with the user
        playlist_data = {
            'name': 'Generated Playlist',  # You can customize the name as needed
            'tracks': recommended_songs
        }
        playlist_serializer = PlaylistSerializer(data=playlist_data)
        if playlist_serializer.is_valid():
            playlist_serializer.save(user=user)
            return Response(playlist_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(playlist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserPlaylistsView(APIView):
    permission_classes = [IsTokenAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user  # Assuming you're using Django's built-in authentication
        playlists = Playlist.objects.filter(user=user)
        # Serialize playlists data and return it in the response
        playlists_data = []  # Assuming you have a serializer to serialize playlist data
        for playlist in playlists:
            playlist_data = {
                'name': playlist.name,
                'tracks': playlist.tracks,
                # Add other fields as needed
            }
            playlists_data.append(playlist_data)
        return Response(playlists_data, status=status.HTTP_200_OK)



    def delete(self, request):
        playlist_user = Playlist.objects.get(user=request.user)
        playlist_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)