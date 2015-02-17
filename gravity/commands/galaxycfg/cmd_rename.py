import os

import click

from gravity import options
from gravity import config_manager
from gravity.io import error


@click.command('reregister')
@options.required_config_arg(name='old_config')
@options.required_config_arg(name='new_config', exists=True)
@click.pass_context
def cli(ctx, old_config, new_config):
    """ Update path of registered config file.

    aliases: rename
    """
    with config_manager.config_manager() as cm:
        try:
            cm.rename(old_config, new_config)
        except Exception as exc:
            error('Caught exception: %s', exc)
