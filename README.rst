######################
rpi-rfsniffer
######################

Allows you to record RF signals and play them back on a Rapsberry Pi.

Nowadays, many remotes are sending over cheap RF transmitters. Especially
alot of the home automation devices usually communicate over these RF links.

######################
Installation
######################

Through pip::

    $>sudo pip install rpi-rfsniffer


Latest development version (in linux)::

    $>git clone https://github.com/jderehag/rpi-rfsniffer.git
    $>cd rpi-rfsniffer
    $>sudo python setyp.py install
    $>


######################
Usage
######################
By default it assumes you have attached the transmitter on pin 11 and the
recevier on pin 13::

    # To record signal
    $>rfsniffer record remotename.button1
      Press remotename.button1
      Recorded 64 bit transitions
    $>

    # To transmit/send that signal (twice)
    $>rfsniffer play remotename.button1 remotename.button1
    $>

    # To dump all the recorded signals
    $>rfsniffer dump
      remotename.button1
    $>


######################
Hardware guide
######################
|All pin assignments refer to board numbers (rather than chipset pin layout).
|Allthough it has only been tested on RPi2, according to `RPi doc
<https://www.raspberrypi.org/documentation/usage/gpio/>`_ all boards should be pin compatible.
|Worth mentioning is that it is working in pull-down resistor mode. But this should not make any difference for rfsniffer since it simply reads any edge transitions and does not really care about the line level itself.


######################
Signal recording
######################
|Worth mentioning is that rfsniffer only is a thin wrapper around `RPi.GPIO <https://sourceforge.net/projects/raspberry-gpio-python/>_.
|rfsniffer simply reads bitflips using RPi.GPIO.wait_for_edge(..) and records the timing between these transitions.
|It ignores any signals with fewer than 5 transitions due to that its assumed that most RF systems have atleast a 5 bit preamble.
|Furthermore, it will continue reading a signal until atleast 1 second has passed without any additional signals. So if you record a buttonpress, you will likely want to release the button as you would normally so that rfsniffer can detect that there are no more signals and then store the signal in the database.
