from pymush.config import Config as BaseConfig
from vmush import conf as django_conf


class Config(BaseConfig):

    def __init__(self):
        super().__init__()
        self.process_name = "VMUSH Server"
        self.django_settings = django_conf

    def setup(self):
        super().setup()
        self._config_django()
        self._load_django()

    def _config_classes(self):
        super()._config_classes()
        self.classes['game']['connection'] = "vmush.conn.Connection"
        self.classes["game"]["gamesession"] = "vmush.conn.GameSession"

        self.classes['gameobject']['ALLIANCE'] = 'vmush.db.objects.alliance.Alliance'
        self.classes['gameobject']['BOARD'] = 'vmush.db.objects.board.Board'
        self.classes['gameobject']['CHANNEL'] = 'vmush.db.objects.channel.Channel'
        self.classes['gameobject']['DIMENSION'] = 'vmush.db.objects.dimension.Dimension'
        self.classes['gameobject']['DISTRICT'] = 'vmush.db.objects.district.District'
        self.classes['gameobject']['FACTION'] = 'vmush.db.objects.faction.Faction'
        self.classes['gameobject']['GATEWAY'] = 'vmush.db.objects.gateway.Gateway'
        self.classes['gameobject']['HEAVENLYBODY'] = 'vmush.db.objects.heavenlybody.HeavenlyBody'
        self.classes['gameobject']['ITEM'] = 'vmush.db.objects.item.Item'
        self.classes['gameobject']['MOBILE'] = 'vmush.db.objects.mobile.Mobile'
        self.classes['gameobject']['SECTOR'] = 'vmush.db.objects.sector.Sector'
        self.classes['gameobject']['VEHICLE'] = 'vmush.db.objects.vehicle.Vehicle'
        self.classes['gameobject']['WILDERNESS'] = 'vmush.db.objects.wilderness.Wilderness'

    def _config_django(self):
        d = self.django_settings

        d.INSTALLED_APPS = [
            'vmush'
        ]

        d.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'gamedb.sqlite3'
        }

    def _load_django(self):
        from django.conf import settings
        settings.configure(self.django_settings)
        import django
        django.setup()

    def _config_matchers(self):
        super()._config_matchers()
        m = self.command_matchers
        m['login']['login'] = 'vmush.engine.commands.login.LoginCommandMatcher'