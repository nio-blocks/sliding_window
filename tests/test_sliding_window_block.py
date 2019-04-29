from time import sleep

from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..sliding_window_block import SlidingWindow

class TestSlidingWindow(NIOBlockTestCase):

    def test_collect(self):
        block = SlidingWindow()
        self.configure_block(block, {
            'min_signals': 1,
            'max_signals': 4
        })
        block.start()
        block.process_signals([Signal])
        self.assert_num_signals_notified(1, block)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(3, block)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(6, block)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(10, block)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(14, block)


    def test_min_signals(self):
        block = SlidingWindow()
        self.configure_block(block, {
            'min_signals': 3,
            'max_signals': 4
        })
        block.start()
        block.process_signals([Signal()])
        block.process_signals([Signal()])
        self.assert_num_signals_notified(0, block)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(3, block)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(7, block)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(11, block)

    def test_multi_signals(self):
        block = SlidingWindow()
        self.configure_block(block, {
            'min_signals': 3,
            'max_signals': 4
        })
        block.start()
        first = Signal()
        last = Signal()
        block.process_signals([Signal(), first, Signal(), Signal(), last])
        self.assert_num_signals_notified(4)
        self.assertTrue(self.last_notified[DEFAULT_TERMINAL][0] is first)
        self.assertTrue(self.last_notified[DEFAULT_TERMINAL][3] is last)

    def test_window_slide(self):
        block = SlidingWindow()
        self.configure_block(block, {
            'min_signals': 3,
            'max_signals': 4
        })
        block.start()
        first = Signal()
        marker = Signal()
        block.process_signals([Signal(), Signal(), Signal(), marker])
        self.assertTrue(
            self.last_notified[DEFAULT_TERMINAL][-4:][-1] is marker)
        block.process_signals([Signal()])
        self.assertTrue(self.last_notified[DEFAULT_TERMINAL][-4:][2] is marker)
        block.process_signals([Signal()])
        self.assertTrue(self.last_notified[DEFAULT_TERMINAL][-4:][1] is marker)
        block.process_signals([Signal()])
        self.assertTrue(self.last_notified[DEFAULT_TERMINAL][-4:][0] is marker)
        block.process_signals([Signal()])
        self.assertTrue(
            self.last_notified[DEFAULT_TERMINAL][-4:][0] is not marker)

    def test_min_expiration(self):
        block = SlidingWindow()
        self.configure_block(block, {
            'min_signals': 1,
            'max_signals': 4,
            'expiration': { 'milliseconds': 200 }
        })

        block.start()
        block.process_signals([Signal(), Signal(), Signal(), Signal()])
        self.assert_num_signals_notified(4, block)
        sleep(.3)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(5, block)

    def test_zero_expiration(self):
        block = SlidingWindow()
        self.configure_block(block, {
            'min_signals': 1,
            'max_signals': 2,
            'expiration': {'seconds': 0}
        })
        block.start()
        block.process_signals([Signal])
        self.assert_num_signals_notified(1, block)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(2, block)
