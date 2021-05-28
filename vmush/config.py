from pymush.config import Config as BaseConfig


class Config(BaseConfig):

    def __init__(self):
        super().__init__()
        self.process_name = "VMUSH Server"

    def _config_classes(self):
        super()._config_classes()
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