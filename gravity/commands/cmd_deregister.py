import os

import click

from gravity import options
from gravity import config_manager
from gravity.io import error


@click.command('deregister')
@click.argument('instance')
@options.required_config_arg(nargs=-1)
@click.pass_context
def cli(ctx, instance, config):
    """ Deregister config file(s).

    aliases: remove, forget
    """
    with config_manager.config_manager() as cm:
        try:
            cm.remove(instance, config)
        except Exception as exc:
            error('Caught exception: %s', exc)
            ctx.exit(1)
