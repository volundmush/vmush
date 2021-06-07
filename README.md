# VMUSH - A MUSH and MUD Platform for Python

## WARNING: Early Alpha!
Pardon our dust, this project is still in its infancy. It kinda runs, but if you're not a developer intent on sprucing it up, it may not have much for you just yet.

## CONTACT INFO
**Name:** Volund

**Email:** volundmush@gmail.com

**PayPal:** volundmush@gmail.com

**Discord:** Volund#1206  

**Discord Channel:** https://discord.gg/Sxuz3QNU8U

**Patreon:** https://www.patreon.com/volund

**Home Repository:** https://github.com/volundmush/pymush

## TERMS AND CONDITIONS

MIT license. In short: go nuts, but give credit where credit is due.

Please see the included LICENSE.txt for the legalese.

## INTRO
Building off the solid MUSH framework provided by [PyMUSH](https://github.com/volundmush/pymush) , VMUSH is a working implementation of PyMUSH, meant to be the successor to the popular [Volund MUSHCode Suite](https://github.com/volundmush/mushcode) but with a few twists to make it suitable for MUDs as well as MUSHes.

## FEATURES
 * Coming soon...

## OKAY, BUT HOW DO I USE IT?
Glad you asked!

You can install vmush using ```pip install vmush```

This adds the `vmush` command to your shell. use `vmush --help` to see what it can do.

The way that athanor and projects built on it work:

`vmush --init <folder>` will create a folder that contains your game's configuration, save files, database, and possibly some code. Enter the folder and use `vmush start` and `vmush stop` to control it. you can use `--app server` or `--app portal` to start/stop specific programs.

Do note that VMUSH is built upon Django, so `vmush migrate` is needed to create the initial database.

Examine the appdata/config.py and portal.py and server.py - which get their initial configuration from pymush's defaults - for how to change the server's configuration around.


## OKAAAAAAY, SO HOW DO I -REALLY- USE IT?
The <folder> created by --init must be filled with Python code and configuration changes fit for your game (or, alternatively, code can be put 'anywhere' as long as it's visible on the Python path), then any further changes needed must be implemented in MUSHcode. Be sure to keep backups of this folder!

What, that still isn't enough? Well...

VMUSH retains the extendability of the PyMUSH framework it's built upon. Because you can replace any and all classes the program uses for its startup routines, and the launcher itself is a class, it's easy-peasy to create a whole new library with its own command-based launcher and game template that the launcher creates a skeleton of with `--init <folder>`.

Not gonna lie though - that does need some Python skills.

## FAQ 
  __Q:__ This is cool! How can I help?  
  __A:__ [Patreon](https://www.patreon.com/volund) support is always welcome. If you can code and have cool ideas or bug fixes, feel free to fork, edit, and pull request! Join our [discord](https://discord.gg/Sxuz3QNU8U) to really get cranking away though.

  __Q:__ I found a bug! What do I do?  
  __A:__ Post it on this GitHub's Issues tracker. I'll see what I can do when I have time. ... or you can try to fix it yourself and submit a Pull Request. That's cool too.

  __Q:__ But... I want a MUD! Where do I start making a MUD?  
  __A:__ check out [vmush](https://github.com/volundmush/vmush)

## Special Thanks
  * The [Evennia](https://www.evennia.com) Project.
  * All of my Patrons on [Patreon](https://www.patreon.com/volund).
  * Anyone who contributes to this project or my other ones.
  * The PennMUSH and RhostMUSH dev teams, especially Ashen-Shugar.