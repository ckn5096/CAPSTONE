from django.contrib import admin

# Register your models here.
from .models import MusicPreference , Playlist

admin.site.register(MusicPreference)
admin.site.register(Playlist)