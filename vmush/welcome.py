from mudstring.encodings.pennmush import ansi_fun
from pymush.utils.welcome import instructions, instructions2, instructions3, instructions4

logo = ansi_fun("hy", r"""
           ___________/\___________                   
         __\      __  /\  __      /_____________________________________
        |   ______\ \ || / /   /\    ____ ________ _______  ______      |
        |   \ ____|\ \||/ /   /  \   \  | | _  _ | \   ___| \  __ \     |
        |   | |     \ \/ /   / /\ \   | | |/ || \|  | |      | | \ |    |
        |   | |______\  /___/ /__\ \  | |    ||     | |______| |__||    |
       <   <  _______ () ___  ____  > | |    ||     |  ______| |__||>    >
        |   | |      /  \   ||    ||  | |    ||     | |      | |  ||    |
        |   | |_____/ /\ \  ||    ||  | |__  ||     | |___   | |_/ |    |
        |   /______/ /||\ \/_|    |_\ /____\/__\   /______| /_____/     |
        |___      /_/ || \_\       _____________________________________|
           /__________\/__________\                     """) + ansi_fun("hr", "M U S H") + ansi_fun("hy", """
                      \\/
------------------------------------------------------------------------------\n""")


last_line = ansi_fun("hy", "------------------------------------------------------------------------------")

message = logo + instructions + instructions2 + instructions3 + instructions4 + last_line