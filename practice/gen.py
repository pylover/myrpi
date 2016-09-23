

import contextlib


@contextlib.contextmanager
def ctx():
    print('Before')

    def _generator():
        for n in range(10):
            yield n

    yield _generator()

    print('After')


if __name__ == '__main__':
    with ctx() as g:
        for i in g:
            print(i)
