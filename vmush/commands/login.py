import re
from vmush.db.importer import Importer
from vmush.db.flatfile import check_password
from pymush.commands.base import (
    Command,
    CommandException,
    PythonCommandMatcher,
)
from pymush.commands.login import (
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
        results = await self.db.list_objects(type_name='PLAYER')
        character, error = await self.entry.game.search_objects(
            name, candidates=results.data, exact=True
        )
        if error:
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not character:
            raise CommandException("Sorry, that was an incorrect username or password.")
        key, char_data = character
        result = await self.db.get_object_attribute(key, name="XYXXY")
        if not (old_hash_attr := result.data):
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not check_password(old_hash_attr['value'].plain, password):
            raise CommandException("Sorry, that was an incorrect username or password.")
        print(f"what is: {char_data}")
        result = await self.db.get_user(char_data['user'])
        print(f"What is result: {result}")
        if not result.data:
            raise CommandException(
                "Character found! However this character has no account. To continue, create an account and bind the character after logging in."
            )
        user = result.data

        await self.entry.login(user, skip_password=True)

        self.entry.msg(
            text=f"Your Account password has been set to the password you entered just now.\n"
            f"Next time, you can login using the normal connect command.\n"
            f"pconnect will not work on your currently bound characters again.\n"
            f"If any imported characters are not appearing, try @pbind <name>=<password>\n"
            f"Should that fail, contact an administrator."
        )

        hash_pass = self.game.crypt_con.hash(password)
        await self.db.update_user(key=user['uuid'], password_hash=hash_pass)

        for char in await self.db.list_objects(user=user['uuid']).data:
            await self.db.set_object_attribute(char, name='XYXXY', value=None)


class LoginCommandMatcher(OldCmdMatcher):
    def at_cmdmatcher_creation(self):
        super().at_cmdmatcher_creation()
        self.add(PennConnect)
        self.add(ImportCommand)
