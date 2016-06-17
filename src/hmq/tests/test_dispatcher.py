import unittest
from hmq.tests.aio import AioTestCase


class TestDispatcher(AioTestCase):

    def test_easy(self):
        self.assertEqual(1, 1)

    async def test_complex(self):
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
