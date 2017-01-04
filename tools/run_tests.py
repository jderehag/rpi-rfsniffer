#!/usr/bin/env python
'''
Copyright (c) 2017, Jesper Derehag <jderehag@hotmail.com>
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
import logging
import os
import sys
import unittest


def run_tests(args, path, pattern):
    print('Running unittests', pattern, 'in', path)
    loader = unittest.TestLoader().discover(start_dir=path, pattern=pattern)
    runner = unittest.runner.TextTestRunner(descriptions=not args.quicktest)
    return runner.run(loader).wasSuccessful()


def main():
    parser = argparse.ArgumentParser(description="Runner for all unittests",
                                     add_help=True)
    parser.add_argument('-v', action="store_true", dest='verbose',
                        default=False, help="enable logger, in DEBUG")
    parser.add_argument('-q', action="store_true", dest='quicktest',
                        default=False,
                        help='Quicktest - suitable for commit-hooks')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not run_tests(args, path=utils.repo_root(), pattern='test*.py'):
        print('Unittests failed, fix your crap and rerun', __file__)
        exit(-1)


if __name__ == '__main__':
    # This sys.path shenanigan is to allow absolute imports of utils
    # Unfortunatly relative does not work for non-package imports
    this_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(this_dir, os.pardir))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    from tools import utils

    main()
