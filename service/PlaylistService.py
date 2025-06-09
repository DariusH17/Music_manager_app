from repository.PlaylistRepository import PlaylistRepository
from service.YouTubeAudioPlayer import YouTubeAudioPlayer
from random import shuffle


class PlaylistService:
    def __init__(self, playlist : PlaylistRepository, player : YouTubeAudioPlayer):
        self.__playlist = playlist
        self.__player = player

    def add_song(self, new_song):
        self.__playlist.add_song(new_song)

    def remove_song(self, song_to_remove):
        self.__playlist.remove_song(song_to_remove)

    def get_all_songs(self):
        return self.__playlist.get_all_songs()

    def play(self):
        for song in self.get_all_songs():
            self.__player.enqueue(song)
        self.__player.play()

    def play_any_song(self, song_to_play):
        self.__player.enqueue(song_to_play)
        self.__player.play()

    def shuffle_songs(self):
        shuffle(self.get_all_songs())

    def skip_song(self):
        self.__player.skip()

