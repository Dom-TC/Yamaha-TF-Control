# Yamaha-TF-Control

This is a collection of Python scripts for controlling Yamaha TF series consoles over a network.  An example QLab file is included to show how you might intergrate the script with your show.

These scripts require Python 3.6 or later, so when first run you may be asked to install Apple's Command Line Tools.  Install them and then retry.

## fade.py
This script, surprisingly, lets you fade a given DCA.

To use it run `python3 fade.py -d <dca> -l <level> -t <fadetime>`.  For example, to fade DCA 1 to -25 over 7 seconds, you'd use the command `fade.py -d 1 -l -25 -t 7`.

## server.py
For offline programming, a server application is included that mocks the TF-Rack, sending back the expected responses as the TF-Rack would.  To use it, change the IP address in your script to `localhost` and run `python3 server.py` in a second terminal window, before running the relevant script. 
