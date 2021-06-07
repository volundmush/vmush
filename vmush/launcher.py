from athanor.launcher import AthanorLauncher
import os
import vmush


class VMUSHLauncher(AthanorLauncher):
    name = "VMUSH"
    root = os.path.abspath(os.path.dirname(vmush.__file__))
    game_template = os.path.abspath(
        os.path.join(os.path.abspath(os.path.dirname(vmush.__file__)), 'game_template'))

    def operation_passthru(self, op, args, unknown):
        """
        Some wizardry that will enable the VMUSH launcher to run Django management commands. example:

        vmush makemigrations
        """
        from appdata.server import Config
        c = Config()
        c.setup()
        print(c.django_settings)
        from django.core import management
        management.call_command(*([op] + unknown))