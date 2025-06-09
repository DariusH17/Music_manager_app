from domain.exception import CustomException


class PlaylistRepository:
    def __init__(self):
        self.__Playlist = ["viva la vida" , "faded", "counting stars", "pierdut buletinul", "minim doi", "gipsy rock"]

    def add_song(self, new_song):
        for song in self.__Playlist:
            if new_song == song:
                raise CustomException(f'The song {new_song} already exists!')
        self.__Playlist.append(new_song)

    def remove_song(self, song_to_remove):
        for song in self.__Playlist:
            if song == song_to_remove:
                self.__Playlist.remove(song)

    def get_all_songs(self):
        return self.__Playlist