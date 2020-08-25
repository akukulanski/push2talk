# push2talk

## Requirements

* GNU/Linux (wasn't tested in other platforms)
* PulseAudio
* pynput (`pip install pynput`)

## Info

Python script to have easy push2talk functionality. The script daemonizes
itself and listens for specific keypresses:
* Activate push2talk: `<ctrl>+p`
* Deactivate push2talk: `<alt>+p`
* Push2talk key: `<pause>`

The shortcuts are hardcoded (sorry), but the value can easily be changed in
`push2talk/push2talk.py`.

Launch:

```bash
python3 -m push2talk.push2talk start
```

Stop:

```bash
python3 -m push2talk.push2talk stop
```

Status:
```bash
python3 -m push2talk.push2talk status
```


Next improvements:
* installable package (+ launch when boot)
* config file with shortcuts
* some kind of notification when enabled/disabled