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

shortcuts = {'base': keyboard.Key.pause,
             'enable': keyboard.Key.ctrl_l,
             'disable': keyboard.Key.ctrl_r}

_device = 0

def toggle(device):
    # print('toggle')
    os.system(f'pactl set-source-mute {device} toggle')

def mute(device):
    print('mute')
    toggle(device)

def unmute(device):
    print('unmute')
    toggle(device)

class Push2Talk(Daemon):

    pressed_keys = []
    enabled = True

    def _pressed(self, key):
        print(f'key={key}')
        if key not in self.pressed_keys:
            self.pressed_keys.append(key)
            if key == shortcuts['base']:
                if key['enable'] in self.pressed_keys:
                    self.enabled = True
                elif key['disable'] in self.pressed_keys:
                    self.enabled = False
                elif self.enabled:
                    unmute(_device)

    def _released(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
            if key == shortcuts['base']:
                if self.enabled:
                    mute(_device)

    def on_press(self, key):
        try:
            print(f'alphanumeric key {key.char} pressed')
        except AttributeError:
            print(f'special key {key} pressed')
        if key in shortcuts.values():
            self._pressed(key)

    def on_release(self, key):
        print(f'{key} released')
        if key == keyboard.Key.esc:
            # Stop listener
            return False
        if key in shortcuts.values():
            self._released(key)

    def run(self):
        with keyboard.Listener(on_press=self.on_press,
                               on_release=self.on_release) as listener:
            listener.join()


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
