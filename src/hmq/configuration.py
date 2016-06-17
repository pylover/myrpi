# -*- coding: utf-8 -*-
from pymlconf import DeferredConfigManager

__author__ = 'vahid'


__builtin_config = """

debug: true

pool:
    maxsize: 10

"""

settings = DeferredConfigManager()


def init(directories=None, files=None, force=False):
    """
    Initialize the configuration manager
    :param directories: semi-colon separated `string` or `list` of director(y|es)
    :param files: semi-colon separated `string` or `list` of file(s)
    :param force: force initialization even if it's already initialized
    """

    context = {

    }

    settings.load(
        init_value=__builtin_config,
        dirs=directories,
        files=files,
        force=force,
        context=context
    )

    return settings
