import asyncio

from hmq.configuration import settings, init as init_config
from hmq.dispatcher import Dispatcher
from hmq.pool import WorkerPool


def main(config_file):
    init_config(files=config_file)
    loop = asyncio.get_event_loop()
    dispatcher = Dispatcher(config_files=settings.rule_files)
    pool = WorkerPool(dispatcher)
    loop.run_until_complete(pool.run())

