from athanor.utils import partial_match
from pymush.utils.text import truthy
from .flatfile import PennDB
from mudrich.text import Text
from collections import defaultdict
from typing import Union, List, Tuple, Dict, Optional
from uuid import UUID


class VolDB(PennDB):
    def __init__(self):
        super().__init__()
        self.ccp = None

    def cobj(self, abbr):
        if self.ccp is None:
            if not (
                code_object := partial_match(
                    "Core Code Parent <CCP>",
                    self.objects.values(),
                    key=lambda x: x.name,
                )
            ):
                raise Exception("Oops. No Core Code Parent in database!")
            self.ccp = code_object
        if not (attr := self.ccp.get(f"COBJ`{abbr.upper()}")):
            return None
        return self.find_obj(attr.value.plain)

    def list_accounts(self):
        if not (account_parent := self.cobj("accounts")):
            return dict()
        return {o.id: o for o in account_parent.children}

    def list_groups(self):
        if not (group_parent := self.cobj("gop")):
            return dict()
        return {o.id: o for o in group_parent.children}

    def list_index(self, number: int):
        return {o.id: o for o in self.type_index.get(number, set())}

    def list_players(self):
        return self.list_index(8)

    def list_rooms(self):
        return self.list_index(1)

    def list_exits(self):
        return self.list_index(4)

    def list_things(self):
        return self.list_index(2)

    def list_districts(self):
        return {
            k: v
            for k, v in self.list_things().items()
            if v.get("D`DISTRICT", inherit=False)
        }


class Importer:
    def __init__(self, connection, path):
        self.db = VolDB.from_outdb(path)
        self.connection = connection
        self.game = connection.game
        connection.penn = self
        self.complete = set()
        self.obj_map = dict()
        self.old_new = dict()
        self.type_map = defaultdict(dict)
        self.user_map: Dict[int, UUID] = dict()
        self.lost_and_found = None

    async def create_obj(self, dbobj, mode):
        orig_attributes = dict(dbobj.attributes)
        aliases = orig_attributes.pop('ALIAS', None)
        attributes = {k: v.value for k, v in orig_attributes.items()}
        name = Text(dbobj.name)
        user = self.user_map.get(dbobj.parent, self.lost_and_found)
        results = await self.game.create_object(type_name=mode, name=name, dbid=dbobj.id, register=False, user=user,
                                                created=dbobj.created, modified=dbobj.modified, attributes=attributes,
                                                no_check_name=True)
        if results.error:
            raise Exception(f"Could not create GameObject for {dbobj}: {results.error}")
        key = results.data

        self.obj_map[dbobj.id] = key
        self.old_new[dbobj] = key
        self.type_map[mode][dbobj.dbref] = key

        return key

    async def import_users(self):
        data = self.db.list_accounts()
        for dbid, dbobj in data.items():
            if '@' in dbobj.name:
                name = f"ImportedAccount_{dbid}"
                email = dbobj.name
            else:
                name = dbobj.name
                can_use, whynot = self.game.db._valid_user_name(name)
                if not can_use:
                    name = f"ImportedAccount_{dbid}"
                email = None
                if (email_attr := dbobj.attributes.get('EMAIL')):
                    if email_attr.value:
                        email = email_attr.value.plain
            admin_level = None
            for obj in dbobj.children:
                if obj.type == 8:
                    if "WIZARD" in obj.flags:
                        admin_level = (
                            max(admin_level, 10)
                            if admin_level is not None
                            else 10
                        )
                    elif "ROYALTY" in obj.flags:
                        admin_level = (
                            max(admin_level, 8)
                            if admin_level is not None
                            else 8
                        )
                    elif (va := obj.attributes.get("V`ADMIN")) :
                        if truthy(va.value):
                            admin_level = (
                                max(admin_level, 6)
                                if admin_level is not None
                                else 6
                            )
            result = await self.game.db.create_user(name=Text(name), email=email, admin_level=admin_level)
            if result.error:
                raise Exception(f"could not import user {dbobj}")
            self.user_map[dbobj.id] = result.data

        result = await self.game.db.create_user(name=Text("LostAndFound"))
        if result.error:
            raise Exception("could not create LostAndFound")
        self.lost_and_found = result.data

    async def import_skeleton(self):
        for data, mode in (
            (self.db.list_accounts(), "USER"),
            (self.db.list_groups(), "FACTION"),
            (self.db.list_districts(), "DISTRICT"),
            (self.db.list_players(), "PLAYER"),
            (self.db.list_rooms(), "ROOM"),
            (self.db.list_exits(), "EXIT"),
            (self.db.list_things(), "THING"),
        ):
            await self.import_bunch(data, mode)

    async def import_bunch(self, data, mode):
        for k, v in data.items():
            if k in self.obj_map:
                continue
            await self.create_obj(v, mode)

    async def process_reverse(self):
        for old, new in self.old_new.items():

            if (zone := self.obj_map.get(old.zone, None)) :
                await self.game.db.set_object_relations(key=new, relation_type='ZONE', target=zone)

            if (parent := self.obj_map.get(old.parent, None)):
                await self.game.db.set_object_relations(key=new, relation_type='PARENT', target=parent)

            if (owner := self.obj_map.get(old.owner, None)):
                await self.game.db.set_object_relations(key=new, relation_type='OWNER', target=owner)

            if old.type == 4:  # an exit
                if (destination := self.obj_map.get(old.location, None)) :
                    await self.game.db.set_object_relations(key=new, relation_type='DESTINATION', target=destination)

                if (location := self.obj_map.get(old.exits, None)) :
                    await self.game.db.set_object_relations(key=new, relation_type='EXITS', target=location)

            else:
                if (location := self.obj_map.get(old.location, None)) :
                    await self.game.db.set_object_relations(key=new, relation_type='LOCATION', target=location)

    async def process_finalize(self):
        for old, new in self.old_new.items():
            await self.game.register_object(new)

    async def run(self):
        try:
            await self.import_users()
            await self.import_skeleton()
            await self.process_reverse()
            await self.process_finalize()
            self.connection.msg("IMPORT COMPLETE!?")
        except Exception as e:
            import traceback, sys

            traceback.print_exc(file=sys.stdout)
            self.connection.msg(f"SOMETHING WENT WRONG: {e}")
