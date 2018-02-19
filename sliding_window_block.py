from collections import defaultdict
from datetime import datetime

from nio.block.base import Block
from nio.properties import IntProperty, VersionProperty, TimeDeltaProperty
from nio.command import command

@command("expire")
class SlidingWindow(Block):
    """Creates a sliding window of signals.

    Examples:

    { min_signals = 1, max_signals = 3 }
    input:  ----1------2--------3--------4--------5-->
    output: ----•------•--------•--------•--------•-->
              [1]  [1,2]  [1,2,3]  [2,3,4]  [3,4,5]


    { min_signals = 3, max_signals = 3 }
    input:  ----1------2--------3--------4--------5-->
    output: --------------------•--------•--------•-->
                          [1,2,3]  [2,3,4]  [3,4,5]


    { min_signals = 1, max_signals = 3, expiration: { millseconds: 500 } }
    input:  ----1------2--------3--------4--| >500ms |---5-->
    output: ----•------•--------•--------•--|        |---•-->
              [1]  [1,2]  [1,2,3]  [2,3,4]             [5]
    """

    """TODO
    - [x] Window Expriation
    - [ ] Implement Group
    - [ ] Implement Persistence
    - [ ] Use Signal Expiration
    """

    version = VersionProperty("0.0.1")
    min_signals = IntProperty(default=1, title='Min Signals')
    max_signals = IntProperty(title='Max Signals')
    expiration = TimeDeltaProperty(title='Window Expiration',
                                   allow_none=True)

    def __init__(self):
        super().__init__()
        self.buffer = []
        self._last_recv = datetime.min

    def expire(self):
        self.logger.debug('Clearing the buffer window')
        self.buffer.clear()

    def process_signals(self, signals):
        now = datetime.utcnow()

        hasExpiration = self.expiration() is not None
        if hasExpiration and (self._last_recv + self.expiration()) < now:
            self.logger.debug('The buffer window has expired')
            self.buffer.clear()

        self._last_recv = now

        for signal in signals:
            self.buffer.append(signal)

        del self.buffer[:-self.max_signals()]

        if len(self.buffer) >= self.min_signals():
            self.notify_signals(self.buffer)
