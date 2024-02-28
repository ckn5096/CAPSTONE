from django.urls import path
from .views import MusicPreferenceView, GeneratePlaylistView, UserPlaylistsView

urlpatterns = [
   # path('register/', RegistrationView.as_view(), name='registration'),
    #path('login/', LoginView.as_view(), name='login'),
    #path('home/', HomeView.as_view(), name='home'),

    path('MusicPreference/', MusicPreferenceView.as_view(), name='MusicPreference'),
    path('generate_playlist/', GeneratePlaylistView.as_view(), name='GeneratePlaylist'),
    path('UserPlaylist/', UserPlaylistsView.as_view(), name='UserPlaylist'),
]

