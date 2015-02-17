import os

import click

from gravity import options
from gravity import config_manager
from gravity.io import error


@click.command('register')
@options.required_config_arg(exists=True, nargs=-1)
@click.pass_context
def cli(ctx, config):
    """ Register config file(s).

    aliases: add
    """
    with config_manager.config_manager() as cm:
        try:
            cm.add(config)
        except Exception as exc:
            error('Caught exception: %s', exc)
