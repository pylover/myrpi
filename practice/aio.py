# grep.py
#
# A very simple coroutine
# http://www.dabeaz.com/coroutines/


def grep(pattern):
    print("Looking for %s" % pattern)
    line = yield
    while True:
        line = yield '%s: %s' % ('Found' if pattern in line else 'Not Found!', line)


# Example use
if __name__ == '__main__':
    g = grep("python")
    next(g)
    print(g.send("Yeah, but no, but yeah, but no"))
    print(g.send("A series of tubes"))
    print(g.send("python generators rock!"))
