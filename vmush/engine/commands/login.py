import re
from vmush.db.importer import Importer
from vmush.db.flatfile import check_password
from pymush.engine.commands.base import (
    Command,
    MushCommand,
    CommandException,
    PythonCommandMatcher,
)
from pymush.engine.commands.login import (
    _LoginCommand,
    LoginCommandMatcher as OldCmdMatcher,
)
from mudrich.encodings.pennmush import ansi_fun, send_menu


class ImportCommand(Command):
    name = "@import"
    re_match = re.compile(r"^(?P<cmd>@import)(?: +(?P<args>.+)?)?", flags=re.IGNORECASE)
    help_category = "System"

    @classmethod
    async def access(cls, entry):
        if entry.game.objects:
            return False
        return True

    async def execute(self):
        penn = Importer(self.entry, "outdb")
        self.entry.msg(f"Database loaded: {len(penn.db.objects)} objects detected!")
        await penn.run()


class PennConnect(_LoginCommand):
    """
    This command will access a PennMUSH character and login using their
    old password. This will then initialize the imported Account and
    log you in.

    Usage:
        pconnect <character> <password>

    If a character name contains spaces, then:
        pconnect "<character name>" password
    """

    name = "pconnect"
    re_match = re.compile(r"^(?P<cmd>pconnect)(?: +(?P<args>.+))?", flags=re.IGNORECASE)
    usage = (
        "Usage: "
        + ansi_fun("hw", "pconnect <username> <password>")
        + " or "
        + ansi_fun("hw", 'pconnect "<user name>" password')
    )

    async def execute(self):
        name, password = self.parse_login(self.usage)
        candidates = self.entry.game.type_index["PLAYER"]
        character, error = self.entry.game.search_objects(
            name, candidates=candidates, exact=True
        )
        if error:
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not character:
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not (old_hash_attr := character.attributes.get("XYXXY")):
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not check_password(old_hash_attr.value.plain, password):
            raise CommandException("Sorry, that was an incorrect username or password.")
        root_owner = character.root_owner
        if not root_owner:
            raise CommandException(
                "Character found! However this character has no account. To continue, create an account and bind the character after logging in."
            )
        if not root_owner.type_name == "USER":
            raise CommandException(
                "Character found! However this character has no account. To continue, create an account and bind the character after logging in."
            )
        await self.entry.login(root_owner)

        self.entry.msg(
            text=f"Your Account password has been set to the password you entered just now.\n"
            f"Next time, you can login using the normal connect command.\n"
            f"pconnect will not work on your currently bound characters again.\n"
            f"If any imported characters are not appearing, try @pbind <name>=<password>\n"
            f"Should that fail, contact an administrator."
        )
        await root_owner.change_password(password)
        for char in root_owner._owner_of_type["PLAYER"].values():
            char.attributes.wipe("XYXXY")


class LoginCommandMatcher(OldCmdMatcher):
    def at_cmdmatcher_creation(self):
        super().at_cmdmatcher_creation()
        self.add(PennConnect)
        self.add(ImportCommand)
