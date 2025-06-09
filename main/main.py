from service.YouTubeAudioPlayer import YouTubeAudioPlayer
from ui.ConsoleUI import ConsoleUI
from repository.PlaylistRepository import PlaylistRepository
from service.PlaylistService import PlaylistService

playlist_repository = PlaylistRepository()
player = YouTubeAudioPlayer()
playlist_service = PlaylistService(playlist_repository, player)
ui = ConsoleUI(playlist_service)

ui.run()
