import unittest

from hmq.dispatcher import Dispatcher
from hmq.listener import Listener
from hmq.message import Message
from hmq.tests import AioTestCase


class TestDispatcher(AioTestCase):

    async def test_dispatch(self):
        listener1_callback1_called, \
            listener1_callback2_called, \
            listener2_callback1_called = False, False, False

        listener1 = Listener('test_listener1')
        listener2 = Listener('test_listener2')
        dispatcher = Dispatcher(config="""
            rules:
              test_message_type:
                listeners:
                  - test_listener1
                  - test_listener2
        """)
        dispatcher.register(listener1)
        dispatcher.register(listener2)

        @listener1.bind
        async def listener1_callback1(message: Message):
            nonlocal listener1_callback1_called
            listener1_callback1_called = True
            self.assertEqual(message.data, 'test_data')

        @listener1.bind
        def listener1_callback2(message: Message):
            nonlocal listener1_callback2_called
            listener1_callback2_called = True
            self.assertEqual(message.data, 'test_data')

        @listener2.bind
        def listener2_callback1(message: Message):
            nonlocal listener2_callback1_called
            listener2_callback1_called = True
            self.assertEqual(message.data, 'test_data')

        await dispatcher.dispatch(Message('test_message_type', data='test_data'))

        self.assertTrue(
            listener1_callback1_called and
            listener1_callback2_called and
            listener2_callback1_called
        )


if __name__ == '__main__':
    unittest.main()
