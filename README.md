To reproduce the problem:

* In the repo directory, run `nvim -u init.vim tmp.txt`
* Run `:Womp`
* Make smaller edits to the line, and observe:
  * Whenever the plugin echoes an even number of calls, a highlight appears, and vanishes
    an odd numbers

The problem: The code is written such that a highlight should appear whenever the
number of calls is odd, and should vanish on even numbers.
