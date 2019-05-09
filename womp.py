#!/usr/bin/env python3
import os
import re
import sys
from functools import partial

import neovim

def handle_request(nvim, name, args):
    return

def handle_notification(nvim, name, args):
    if name == 'quit':
        error_cb(nvim, "Got quit")
        sys.exit(0)

    if name == 'do_something':
        nvim.command("echom 'doing something'")

def error_cb(nvim, message):
    with open('nvimlog', 'a') as f:
        f.write('ERROR: %s\n' % (message, ))  # noqa


def main():
    nvim = neovim.attach('stdio')
    error_cb(nvim, "Python script started")

    for buffer in nvim.buffers:
        buffer.api.live_updates(True)

    nvim.run_loop(partial(handle_request, nvim),
                  partial(handle_notification, nvim),
                  err_cb=partial(error_cb, nvim))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        with open('nvimlog', 'a') as f:
            import sys
            import traceback
            f.write("".join(traceback.format_exception(*sys.exc_info())))
