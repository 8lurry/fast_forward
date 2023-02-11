# -*- coding: UTF-8 -*-
# Copyright 2022 8lurry <sharifmehedi24@outlook.com>
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Tailored from: https://gist.github.com/WangYihang/e7d36b744557e4673d2157499f6c6b5e

import sys
from .setup_info import SETUP_INFO
from .local import main as local
from .remote import main as remote

__version__ = SETUP_INFO.get('version')


def main():
    if '--local' in sys.argv:
        sys.argv.remove('--local')
        local()
    else:
        remote()

