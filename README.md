# Yamaha-TF-Control

This is a collection of Python scripts for controlling Yamaha TF series consoles over a network. An example QLab file is included to show how you might intergrate the script with your show.

# Installation

To use these scripts, copy the command you require from the `scripts` folder onto your computer. In each script, update the ip address under the `Console Details` heading towards the top of the file. For example, `ip = "192.168.1.1`. When programming offline, use `localhost`.

These scripts require Python 3.6 or later, so when first run you may be asked to install Apple's Command Line Tools. Install them and then retry.

## fadeDCA.py

```
usage: fadeDCA [-h] [-v] -d <dca> -l <level> -t <duration>

Fade a DCA on a Yamaha TF-series sound console.

options:
  -h, --help            show this help message and exit
  -v, --version         returns the version number
  -d <dca>, --dca <dca>
                        the DCA to fade
  -l <level>, --level <level>
                        the target level
  -t <duration>, --time <duration>
                        the fade duration
```

## recallScene.py

```
usage: fadeDCA [-h] [-v] -d <dca> -l <level> -t <duration>

Fade a DCA on a Yamaha TF-series sound console.

options:
  -h, --help            show this help message and exit
  -v, --version         returns the version number
  -d <dca>, --dca <dca>
                        the DCA to fade
  -l <level>, --level <level>
                        the target level
  -t <duration>, --time <duration>
                        the fade duration
```

## setMuteMaster.py

```
usage: setMuteMaster [-h] [-v] [-m <master>] -s <state>

Sets the input and fx mute masters on a Yamaha TF-series sound console.

options:
  -h, --help            show this help message and exit
  -v, --version         returns the version number
  -m <master>, --master <master>
                        the mute master to be set
  -s <state>, --state <state>
                        the state to set the mute master to
```

## server.py

For offline programming, a server application is included that mocks the TF-Rack, sending back the expected responses as the TF-Rack would. To use it, change the IP address in your script to `localhost` and run `python3 server.py` in a second terminal window, before running the relevant script.

The server will return every channel to be at `-130dB`.
