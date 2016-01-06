Inspired on:
https://www.fyears.org/2015/06/electron-as-gui-of-python-apps.html

I'm using nodeenv (python package) to install node/npm

commands:
    nodeenv --prebuilt node.env
    source node.env/bin/activate

I'm using electron to run the app and electron-packager to build the package.



Resource consumption comparison:

electron html ui: 138.7 MiB ram
cpu (on idle) @ ~0%

bitmask gui: ~170 MiB ram
cpu (idle) @ ~2%
