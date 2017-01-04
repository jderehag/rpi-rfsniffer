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
import os
import shutil


def repo_root():
    '''
    Gets the repo root from utils.py perspective

    Was intially 'git rev-parse --show-toplevel'
    but that for some unkown reason ignores the cwd
    argument when run through check_output.
    So if some script is outside of repo (for
    instance for the commit-hooks) the rev-parse
    is done from inside the .git directory and
    thus fails.

    Returns:
        repo_root(str): Path to the repo root
    '''
    this_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(this_dir, os.pardir))


def install_hooks():
    '''
    This script installs all git hooks into the repo.

    It reads all files in git-hooks and creates copies those to .git/hooks/

    I have also experimented a little bit with gitconfig init.templatedir
    and copying all the hooks. But in the end, that config still needs to be
    set one way or another (git init) so from a usability point of view it
    makes little difference (its not stored on remotes).

    Returns:
        None
    '''
    repo = repo_root()
    hooksdir = os.path.join(repo, 'tools', 'git-hooks')
    for file_ in os.listdir(hooksdir):
        file_ = os.path.join(hooksdir, file_)
        if os.path.isfile(file_):
            # Copy files instead of symlinks because symlinks
            # are unsupported on windows
            shutil.copy(file_, os.path.join(repo, '.git', 'hooks'))
