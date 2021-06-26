from pymush.config import Config as BaseConfig


class Config(BaseConfig):
    def __init__(self):
        super().__init__()
        self.process_name = "VMUSH Server"

    def setup(self):
        super().setup()

    def _config_classes(self):
        super()._config_classes()
        self.classes["game"]["connection"] = "vmush.conn.Connection"
        self.classes["game"]["gamesession"] = "vmush.conn.GameSession"

    def _config_matchers(self):
        super()._config_matchers()
        m = self.command_matchers
        m["login"]["login"] = "vmush.commands.login.LoginCommandMatcher"
