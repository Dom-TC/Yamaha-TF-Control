# Yamaha-TF-Control

This is a collection of Python scripts for controlling Yamaha TF series consoles over a network. An example QLab file is included to show how you might intergrate the script with your show.

# Installation

To use these scripts, copy the command you require from the `scripts` folder onto your computer. In each script, update the ip address under the `Console Details` heading towards the top of the file. For example, `ip = "192.168.1.1`. When programming offline, use `localhost`.

These scripts require Python 3.6 or later, so when first run you may be asked to install Apple's Command Line Tools. Install them and then retry.

## fadeDCA.py

```
usage: fadeDCA [-h] [-v] [-V] -d <dca> -l <level> -t <duration>

Fade a DCA on a Yamaha TF-series sound console.

options:
  -h, --help            show this help message and exit
  -v, --version         returns the version number
  -V, --verbose         output information about the running command
  -d <dca>, --dca <dca>
                        the DCA to fade
  -l <level>, --level <level>
                        the target level
  -t <duration>, --time <duration>
                        the fade duration
```

## muteInput.py

```
usage: set_input_mute [-h] [-v] [-V] -c <channel> -s <state>

Sets the state of an input mute on a Yamaha TF-series sound console.

options:
  -h, --help            show this help message and exit
  -v, --version         returns the version number
  -V, --verbose         output information about the running command
  -c <channel>, --channel <channel>
                        the channel to be muted
  -s <state>, --state <state>
                        the state to set the channel's mute to
```

## recallScene.py

```
usage: recall_scene [-h] [-v] [-V] [-b <bank>] -s <scene>

Recall a scene on a Yamaha TF-series sound console.

options:
  -h, --help            show this help message and exit
  -v, --version         returns the version number
  -V, --verbose         output information about the running command
  -b <bank>, --bank <bank>
                        the scene bank
  -s <scene>, --scene <scene>
                        the scene to recall
```

## setMuteMaster.py

```
usage: set_mute_master [-h] [-v] [-V] [-m <master>] -s <state>

Sets the input and fx mute masters on a Yamaha TF-series sound console.

options:
  -h, --help            show this help message and exit
  -v, --version         returns the version number
  -V, --verbose         output information about the running command
  -m <master>, --master <master>
                        the mute master to be set
  -s <state>, --state <state>
                        the state to set the mute master to
```

## server.py

For offline programming, a server application is included that mocks the TF-Rack, sending back the expected responses as the TF-Rack would. To use it, change the IP address in your script to `localhost` and run `python3 server.py` in a second terminal window, before running the relevant script.

The server will return every channel to be at `-130dB`.
