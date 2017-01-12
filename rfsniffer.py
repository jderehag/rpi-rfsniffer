#!/usr/bin/env python
'''
Copyright (c) 2017, Jesper Derehag
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

from __future__ import print_function
import argparse
import os
import shelve
import time
import warnings

try:
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
except RuntimeError:
    # Catch here so that we can actually test on non-pi targets
    warnings.warn('This can only be executed on Raspberry Pi', RuntimeWarning)


def play(args, buttonsdb):
    GPIO.setup(args.txpin, GPIO.OUT, initial=GPIO.LOW)
    for button in args.button:
        for i, (timing, level) in enumerate(buttonsdb[button]):
            if i is not 0:
                # Busy-sleep (gives a better time granularity than
                # sleep() but at the cost of busy looping)
                now = time.time()
                while now + timing > time.time():
                    pass

            GPIO.output(args.txpin, level)


def read_timings(rx_pin):
    capture = []
    while True:
        start = time.time()
        if GPIO.wait_for_edge(rx_pin, GPIO.BOTH, timeout=1000):
            capture.append((time.time() - start, GPIO.input(rx_pin)))

        elif len(capture) < 5:  # Any pattern is likely larger than 5 bits
            capture = []
        else:
            return capture


def record(args, buttons):
    GPIO.setup(args.rxpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print('Press', args.button)
    sample = read_timings(args.rxpin)
    print('Recorded', len(sample), 'bit transitions')
    buttons[args.button] = sample


def dump(args, buttons):
    for button in sorted(buttons.keys()):
        print(button)
        if args.verbose:
            for timing, toggle in buttons[button]:
                print('\t{0:.6f}'.format(timing), toggle)


def main():
    fc = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(add_help=True, formatter_class=fc)

    subparsers = parser.add_subparsers(help='sub-command help')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        default=False, help='Verbose output')

    parser.add_argument('--rxpin', type=int, default=13,
                        help=('The RPi boardpin where the RF receiver'
                              ' is attached'))

    parser.add_argument('--txpin', type=int, default=11,
                        help=('The RPi boardpin where the RF transmitter'
                              ' is attached'))

    parser.add_argument('-b', '--buttonsdb', dest='buttonsdb',
                        default=os.path.join(os.environ['HOME'],
                                             'buttons.db'))

    # Record subcommand
    parser_record = subparsers.add_parser('record',
                                          help='Record an RF signal')
    parser_record.add_argument('button')
    parser_record.set_defaults(func=record)

    # Play subcommand
    parser_play = subparsers.add_parser('play', help=('Send a previously '
                                                      'recorded RF signal'))
    parser_play.add_argument('button', nargs='*')
    parser_play.set_defaults(func=play)

    # Dump subcommand
    parser_dump = subparsers.add_parser('dump', help=('Dumps the already '
                                                      'recorded RF signals'))
    parser_dump.set_defaults(func=dump)

    args = parser.parse_args()

    buttons = shelve.open(args.buttonsdb)
    args.func(args, buttons)

    buttons.close()
    GPIO.cleanup()


if __name__ == '__main__':
    main()
