#!/usr/bin/env python
# code: utf-8

'''
A wrapper script to generate zip files for GitHub releases.
This script tends to be compatible with both Python 2 and Python 3.
'''

from __future__ import print_function

import os, shutil

DEDRM_SRC_DIR = 'DeDRM_Plugin'
RELEASE_DIR = os.getcwd()

def make_release(version):
    shutil.make_archive(DEDRM_SRC_DIR, 'zip', DEDRM_SRC_DIR)
    release_name = 'DeDRM_plugin_{}'.format(version)
    result = os.rename(DEDRM_SRC_DIR+'.zip',release_name+'.zip')
    return result


if __name__ == '__main__':
    import sys
    try:
        version = sys.argv[1]
    except IndexError:
        raise SystemExit('Usage: {} version'.format(__file__))

    print(make_release(version))