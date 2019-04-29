from collections import defaultdict
from time import monotonic

from nio.block.base import Block
from nio.block.mixins.group_by.group_by import GroupBy
from nio.properties import IntProperty, VersionProperty, TimeDeltaProperty, \
    StringProperty
from nio.command import command

@command('expire')
class SlidingWindow(GroupBy, Block):
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
    - [x] Implement Group
    - [ ] Implement Persistence
    - [x] Use Signal Expiration
    """

    min_signals = IntProperty(default=1, title='Min Signals')
    max_signals = IntProperty(default=20, title='Max Signals')

    expiration = TimeDeltaProperty(default={'seconds': -1},
                                   title='Window Expiration',
                                   advanced=True)
    version = VersionProperty('0.1.0')

    def __init__(self):
        super().__init__()
        self._buffers = defaultdict(list)
        self._last_recv = defaultdict(lambda : monotonic())

    def expire(self):
        self.logger.debug('Clearing the buffer window')
        self._buffers.clear()

    def process_group_signals(self, signals, group, input_id=None):
        now = monotonic()
        delta = now - self._last_recv[group]
        window = self.expiration().total_seconds()
        has_expiration = window >= 0
        is_expired = delta > window or window == 0
        if has_expiration and is_expired:
            self.logger.debug('The buffer window has expired')
            self._buffers[group].clear()

        self._last_recv[group] = now

        for signal in signals:
            self._buffers[group].append(signal)

        del self._buffers[group][:-self.max_signals()]

        if len(self._buffers[group]) >= self.min_signals():
            return self._buffers[group]
