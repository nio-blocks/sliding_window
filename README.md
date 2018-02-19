Sliding Window
===========

Creates a sliding window of signals.

Examples
--------

Basic Usage:

```text
{ min_signals = 1, max_signals = 3 }

input:  ----1------2--------3--------4--------5-->
output: ----•------•--------•--------•--------•-->
          [1]  [1,2]  [1,2,3]  [2,3,4]  [3,4,5]
```

Setting `min_signals`:

```text
{ min_signals = 3, max_signals = 3 }

input:  ----1------2--------3--------4--------5-->
output: --------------------•--------•--------•-->
                      [1,2,3]  [2,3,4]  [3,4,5]
```


Using an `expiration`:

```text
{ min_signals = 1, max_signals = 3, expiration: { millseconds: 500 } }

input:  ----1------2--------3--------4--| >500ms |---5-->
output: ----•------•--------•--------•--|        |---•-->
          [1]  [1,2]  [1,2,3]  [2,3,4]             [5]
```

Properties
--------------
- **min_signals**: Minimum number of signals before the window emits.
- **max_signals**: Maximum number of signals to emit.
- **expiration**: The amount of time the window stays open. After which, if no signals are recieved, then the window is emptied.

Input
-------
- **default**: Any list of signals.

Output
---------
 **default**: A signal group `>= min_signals` and `<= max_signals`


Commands
----------------
- **expire**: Close/expire the window.

Dependencies
----------------
None

