#!/usr/bin/env python3
import os
import re
import sys
import time
from functools import partial

import pynvim as neovim

def handle_request(nvim, name, args):
    time.sleep(0.1)
    return "XYZ"

def handle_notification(nvim, name, args):
    if name == 'quit':
        error_cb(nvim, "Got quit")
        sys.exit(0)

    if name == 'nvim_buf_lines_event':
        nvim.my_counter += 1
        nvim.command("echo \"Number of calls: "+str(nvim.my_counter)+"\"")

        buf = nvim.my_buf
        toggle = nvim.my_counter % 2
        buf.clear_highlight(-1, 0, -1)
        buf.add_highlight("Error", 0, col_start=0, col_end=toggle, src_id=-1, async_=None)


def error_cb(nvim, message):
    with open('nvimlog', 'a') as f:
        f.write('ERROR: %s\n' % (message, ))  # noqa


def main():
    nvim = neovim.attach('stdio')
    error_cb(nvim, "Python script started")

    for buffer in nvim.buffers:
        buffer.api.attach(False, [])

    nvim.my_counter = 0
    nvim.my_buf = nvim.current.buffer
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
