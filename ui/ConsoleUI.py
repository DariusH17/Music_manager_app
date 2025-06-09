from domain.exception import CustomException
from service.PlaylistService import PlaylistService


class ConsoleUI:
    def __init__(self, playlist : PlaylistService):
        self.__playlist = playlist
        self.__commands = {
            "1": self.__play,
            "2": self.__play_a_song,
            "3": self.__shuffle_playlist,
            "4": self.__add_song,
            "5": self.__remove_song,
            "6": self.__show_all_songs,
            "7": self.__skip_song,
        }

    def __print_menu(self):
        print("1. Play")
        print("2. Play a song")
        print("3. Shuffle Playlist")
        print("4. Add song")
        print("5. Remove song")
        print("6. Show all songs")
        print("7. Skip current song")
        print("0. Exit")

    def __play(self):
        self.__playlist.play()

    def __play_a_song(self):
        song_to_play = input("Enter song to play: ")
        self.__playlist.play_any_song(song_to_play)

    def __shuffle_playlist(self):
        self.__playlist.shuffle_songs()
        print("✅")
        self.__show_all_songs()

    def __add_song(self):
        name = input("Enter song name: ")
        self.__playlist.add_song(name)
        self.__show_all_songs()

    def __remove_song(self):
        name = input("Enter song name: ")
        self.__playlist.remove_song(name)
        self.__show_all_songs()

    def __show_all_songs(self):
        print("playlist:\n")
        for song in self.__playlist.get_all_songs():
            print(song)
        print()

    def __skip_song(self):
        self.__playlist.skip_song()

    def run(self):
        print()
        print("Welcome to Music Manager! \n"
              "Here you can manage your music playlist. \n"
              "press 7 to skip current song.\n"
              "after giving a command please wait a bit for the script to connect\n")

        self.__show_all_songs()

        show_menu = True

        while True:
            if show_menu:
                self.__print_menu()

            try:
                print("chose a command:")
                command = input().strip()
                if command == "0":
                    return

                action = self.__commands[command]
                action()

                if command in ("1", "2", "7"):
                    show_menu = False
                else:
                    show_menu = True


            except Exception as error:
                print(" Invalid command!")

            except CustomException as error:
                print(error)
