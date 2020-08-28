# Initially this was done with pure Python using "gi", but it wouldn't
# work since after being "daemonized", since it runs as root it
# won't communicate to user dbus, and notifications won't reach the display.
# See: https://forums.linuxmint.com/viewtopic.php?t=306389
# There is an awful workaround, that consists on run the notify cmd as
# the user and specify the envs DISPLAY and DBUS_SESSION_BUS_ADDRESS.
# See: https://wiki.archlinux.org/index.php/Desktop_notifications#Usage_in_programming
# This code works:
#     sudo -u $USER \
#          DISPLAY=:0 \
#          DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$UID/bus \
#          notify-send 'Hello world!' 'This is an example notification.'
#
# And this is the easy way to do it in the script:
#   os.system("runuser -l <USER_NAME> -c \"export DISPLAY=:0; " \
#             "export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/<USER_ID>/bus; "\
#             "notify-send 'a title' 'a body' --icon=dialog-information")
#
# << Update >>
# My bad (duh), this doesn't run as root! Just setting the envs is enough!
#   os.system("export DISPLAY=:0; " \
#             "export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/<USER_ID>/bus; " \
#             "notify-send 'a title' 'a body' --icon=dialog-information")
#

import os

class Notification:

    _events = {
        'start': {'title': 'Push2Talk daemon running',
                    'body': 'Now you can play control it with shortcuts!',
                    'icon': 'dialog-information'},
        'enabled': {'title': 'Push2Talk enabled',
                    'body': 'Every mic is now muted!',
                    'icon': 'dialog-information'},
        'disabled': {'title': 'Push2Talk disabled',
                     'body': 'Every mic is now unmuted!',
                     'icon': 'dialog-information'},
        'stop': {'title': 'Push2Talk daemon stopped',
                 'body': '',
                 'icon': 'dialog-information'},
    }

    # _runasuser = 'runuser -l {user} -c "{cmd}"'
    _cmd = 'export DISPLAY={display}; ' \
           'export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{uid}/bus; ' \
           'notify-send \'{title}\' \'{body}\' --icon={icon}'

    def __init__(self, display):
        self.display = display

    def send(self, event):
        assert event in self._events
        event = self._events[event]
        os.system(self._cmd.format(uid=os.getuid(),
                                   display=self.display,
                                   title=event['title'],
                                   body=event['body'],
                                   icon=event['icon']))
