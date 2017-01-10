# rpi-rfsniffer

Allows you to record RF signals and play them back on a Rapsberry Pi.

Nowadays, many remotes are sending over cheap RF transmitters. Especially
alot of the home automation devices usually communicate over these RF links.

## Installation

Through pip:
```bash
$>sudo pip install rpi-rfsniffer
```

Latest development version (in linux):
```bash
$>git clone https://github.com/jderehag/rpi-rfsniffer.git
$>cd rpi-rfsniffer
$>sudo python setyp.py install
$>
```

## Usage
By default it assumes you have attached the transmitter on pin 11 and the
recevier on pin 13

```bash
# To record signal
$>rfsniffer record remotename.button1
  Press remotename.button1
  Recorded 64 bit transitions
$>

# To transmit/send that signal
$>rfsniffer play remotename.button1
$>

# To dump all the recorded signals
$>rfsniffer dump
remotename.button1
$>
```


## Hardware guide
TODO


## Signal analysis
TODO

