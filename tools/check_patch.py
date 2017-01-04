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

import os
import sys
import subprocess

ignore_folders = ['.git']
ignore_files = []


def check_flake8(file_):
    '''
    Executes flake8 on file_

    Args:
        file_(str): File to execute flake8 on
    Returns:
        rc(int): Return code for flake8
    '''
    return subprocess.call(['flake8', file_])


def is_valid_file(file_):
    '''
    Checks wether file should be checked or ignored

    Args:
        file_(str): File to execute flake8 on
    Returns:
        valid(Boolean): True if file should be checked
    '''
    if not os.path.isfile(file_):
        return False

    for ignore_folder in ignore_folders:
        if ignore_folder in file_:
            return False

    if os.path.basename(file_) in ignore_files:
        return False

    return True


def find_all_valid_files():
    '''
    Traverses repo from rootdir and finds all files to be checked

    Returns:
        files(list): List of all valid files
    '''
    valid_files = []
    for dirpath, _, files in os.walk(utils.repo_root()):
        for file_ in files:
            file_ = os.path.join(dirpath, file_)
            if is_valid_file(file_):
                valid_files.append(file_)
    return valid_files


def main():
    if len(sys.argv) < 2:
        files = find_all_valid_files()
    else:
        files = [os.path.abspath(file_) for file_ in sys.argv[1:]
                 if is_valid_file(file_)]

    failed_files = []
    for file_ in files:
        # Python checkers
        if file_.endswith('.py'):
            if check_flake8(file_) != 0:
                failed_files.append(file_)

    if len(failed_files) > 0:
        print(os.path.basename(__file__), "failed!")
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
