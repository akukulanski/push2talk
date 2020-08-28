#
# keyboard capture
# https://pynput.readthedocs.io/en/latest/keyboard.html
#
# daemon
# https://web.archive.org/web/20160305151936/http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
#
# mic mute/unmute
# https://www.reddit.com/r/xubuntu/comments/47td2g/mic_muteunmute_toggleable_hotkey/
#

import sys, os
from pynput import keyboard
from .daemon import Daemon
from .notify import Notification

shortcut_enable = '<ctrl>+p'
shortcut_disable = '<alt>+p'
shortcut_toggle = keyboard.Key.pause

_shortcuts = [shortcut_toggle]
_devices = [1, 2]

def set_source_mute(device, status):
    s = {'unmute': '0', 'mute': '1', 'toggle': 'toggle'}
    cmd = f'pactl set-source-mute {device} {s[status]}'
    os.system(cmd)

class Push2Talk(Daemon):

    pressed_keys = []
    enabled = True
    is_pressed = False

    def __init__(self, *args, **kwargs):
        assert os.getuid(), 'Don\'t run as root!'
        display = os.environ['DISPLAY']
        self.notify = Notification(display=display)
        Daemon.__init__(self, *args, **kwargs)

    def on_enable(self):
        if not self.enabled:
            self.enabled = True
            self.notify.send(event='enabled')
            for dev in _devices:
                set_source_mute(dev, 'mute')

    def on_disable(self):
        if self.enabled:
            self.enabled = False
            self.notify.send(event='disabled')
            for dev in _devices:
                set_source_mute(dev, 'unmute')

    def _pressed(self, key):
        if self.enabled:
            if key == shortcut_toggle and not self.is_pressed:
                self.is_pressed = True
                for dev in _devices:
                    set_source_mute(dev, 'unmute')

    def _released(self, key):
        if self.enabled:
            if key == shortcut_toggle:
                self.is_pressed = False
                for dev in _devices:
                    set_source_mute(dev, 'mute')

    def on_press(self, key):
        if key in _shortcuts:
            self._pressed(key)

    def on_release(self, key):
        if key in _shortcuts:
            self._released(key)

    def run(self):
        self.notify.send('start')
        g = keyboard.GlobalHotKeys({shortcut_enable: self.on_enable,
                                    shortcut_disable: self.on_disable})
        l = keyboard.Listener(on_press=self.on_press,
                              on_release=self.on_release)
        g.start()
        l.start()
        g.join()
        l.join()

    def stop(self):
        self.notify.send('stop')
        Daemon.stop(self)


if __name__ == '__main__':
    _cmds = ('start', 'stop', 'restart', 'status')
    assert len(sys.argv) == 2 and sys.argv[1] in _cmds, (
            f'usage: {sys.argv[0]} {"|".join(_cmds)}')
    daemon = Push2Talk('/tmp/push2talk-daemon.pid',
                       stdout='/tmp/stdo', stderr='/tmp/stde')
    if 'start' == sys.argv[1]:
        daemon.start()
    elif 'stop' == sys.argv[1]:
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        daemon.restart()
    elif 'status' == sys.argv[1]:
        print(f'Running: {daemon.is_running()}')
    sys.exit(0)
