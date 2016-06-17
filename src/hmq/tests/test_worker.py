import asyncio
import unittest

from hmq import configuration
from hmq.dispatcher import Dispatcher
from hmq.listener import Listener
from hmq.message import Message
from hmq.pool import WorkerPool
from hmq.tests import AioTestCase


class TestWorker(AioTestCase):

    def setUp(self):
        configuration.init()

    async def test_worker(self):
        listener1_callback1_called, \
            listener1_callback2_called, \
            listener2_callback1_called = 0, 0, 0

        listener1 = Listener('test_listener1')
        listener2 = Listener('test_listener2')
        dispatcher = Dispatcher(config="""
            rules:
              test_message_type_1:
                listeners:
                  - test_listener1
              test_message_type_2:
                listeners:
                  - test_listener2
        """)
        dispatcher.register(listener1)
        dispatcher.register(listener2)

        @listener1.bind
        async def listener1_callback1(message: Message):
            nonlocal listener1_callback1_called
            listener1_callback1_called += 1
            self.assertEqual(message.data['name'], 'test_data')

        @listener1.bind
        def listener1_callback2(message: Message):
            nonlocal listener1_callback2_called
            listener1_callback2_called += 1
            self.assertEqual(message.data['name'], 'test_data')

        @listener2.bind
        def listener2_callback1(message: Message):
            nonlocal listener2_callback1_called
            listener2_callback1_called += 1
            self.assertEqual(message.data['name'], 'test_data')

        pool = WorkerPool(dispatcher)

        async def feeder():
            for i in range(1000):
                await dispatcher.dispatch(Message(
                    'test_message_type_%s' % [1, 2][i % 2],
                    data=dict(name='test_data', index=i)
                ))
            asyncio.sleep(1)
            pool.stop()

        feeder_future = asyncio.ensure_future(feeder())

        await asyncio.gather(pool.run(), feeder_future)

        self.assertEqual(listener1_callback1_called, 500)
        self.assertEqual(listener1_callback2_called, 500)
        self.assertEqual(listener2_callback1_called, 500)


if __name__ == '__main__':
    unittest.main()
