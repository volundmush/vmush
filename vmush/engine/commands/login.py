import re
from vmush.db.importer import Importer
from vmush.db.flatfile import check_password
from pymush.engine.commands.base import Command, MushCommand, CommandException, PythonCommandMatcher
from pymush.engine.commands.login import _LoginCommand, LoginCommandMatcher as OldCmdMatcher
from mudstring.encodings.pennmush import ansi_fun, send_menu


class ImportCommand(Command):
    name = "@import"
    re_match = re.compile(r"^(?P<cmd>@import)(?: +(?P<args>.+)?)?", flags=re.IGNORECASE)
    help_category = 'System'

    @classmethod
    def access(cls, entry):
        if entry.game.objects:
            return False
        return True

    def execute(self):
        penn = Importer(self.entry.enactor, 'outdb')
        self.msg(f"Database loaded: {len(penn.db.objects)} objects detected!")
        penn.run()


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
    name = 'pconnect'
    re_match = re.compile(r"^(?P<cmd>pconnect)(?: +(?P<args>.+))?", flags=re.IGNORECASE)
    usage = "Usage: " + ansi_fun("hw", "pconnect <username> <password>") + " or " + ansi_fun("hw", 'pconnect "<user name>" password')

    def execute(self):
        name, password = self.parse_login(self.usage)
        candidates = self.game.type_index[self.game.obj_classes['PLAYER']]
        character, error = self.game.search_objects(name, candidates=candidates, exact=True)
        if error:
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not character:
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not (old_hash_attr := character.attributes.get('XYXXY')):
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not check_password(old_hash_attr.value.plain, password):
            raise CommandException("Sorry, that was an incorrect username or password.")
        if not (acc := character.account):
            raise CommandException("Character found! However this character has no account. To continue, create an account and bind the character after logging in.")
        self.entry.connection.login(acc)

        self.msg(text=f"Your Account password has been set to the password you entered just now.\n"
                      f"Next time, you can login using the normal connect command.\n"
                      f"pconnect will not work on your currently bound characters again.\n"
                      f"If any imported characters are not appearing, try @pbind <name>=<password>\n"
                      f"Should that fail, contact an administrator.")
        acc.change_password(password)
        for char in acc.characters:
            char.attributes.wipe('XYXXY')


class LoginCommandMatcher(OldCmdMatcher):

    def at_cmdmatcher_creation(self):
        super().at_cmdmatcher_creation()
        self.add(PennConnect)
        self.add(ImportCommand)
