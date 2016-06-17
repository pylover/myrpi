from setuptools import setup as setuptools_setup, find_packages


dependencies = [
    'pymlconf',
    'daemonize',
]


# pycharm inspection fix-up: redirecting `requirements` to `install_requires`
def setup(**kw):
    kw['install_requires'] = kw['requires']
    del kw['requires']
    setuptools_setup(**kw)


setup(
    name='HMQ',
    requires=dependencies,
    packages=find_packages(),
)
