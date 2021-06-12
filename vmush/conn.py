from pymush.conn import GameSession as OldSession, Connection as OldConnection
from .selectscreen import render_select_screen
from .welcome import message as WELCOME


class GameSession(OldSession):
    def show_select_screen(self):
        self.receive_msg(render_select_screen(self))


class Connection(OldConnection):
    def show_welcome_screen(self):
        self.print(WELCOME)
