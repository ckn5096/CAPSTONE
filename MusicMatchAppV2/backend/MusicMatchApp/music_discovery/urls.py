from django.urls import path
from .views import MusicPreferenceView, GeneratePlaylistView, UserPlaylistsView , SpotifyLoginView , SpotifyCallbackView, ListeningHistoryView

urlpatterns = [
   # path('register/', RegistrationView.as_view(), name='registration'),
    #path('login/', LoginView.as_view(), name='login'),
    #path('home/', HomeView.as_view(), name='home'),

    path('MusicPreference/', MusicPreferenceView.as_view(), name='MusicPreference'),
    path('generate_playlist/', GeneratePlaylistView.as_view(), name='GeneratePlaylist'),
    path('UserPlaylist/', UserPlaylistsView.as_view(), name='UserPlaylist'),
    path('api/Spotify/login', SpotifyLoginView.as_view(), name='SpotifyLogin'),
    path('spotify-callback/', SpotifyCallbackView.as_view(), name='spotify_callback'),
    path('api/ListeningHistory/', ListeningHistoryView.as_view(), name='ListeningHistory'),
]

