Sliding Window
===========

Creates a sliding window of signals, so that for every list of signals processed a new list is emitted that contains the previous *x* signals, where **Min Signals** <= *x* <= **Max Signals**.

Properties
--------------
- **Min Signals**: Minimum number of signals before the window emits.
- **Max Signals**: Maximum number of signals to emit.
- **Window Expiration**: The amount of time the window stays open. After which, if no signals are recieved, then the window is emptied.

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

Outputs
---------
A list of previously received signals with length `>= min_signals` and `<= max_signals`.

Commands
----------------
- **expire**: Close/expire the window.
