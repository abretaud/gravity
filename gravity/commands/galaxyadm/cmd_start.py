import os

import click

from gravity import options
from gravity import process_manager

@click.command('start')
@options.required_instance_arg()
@click.pass_context
def cli(ctx, instance):
    """ Start configured services.
    """
    with process_manager.process_manager() as pm:
        pm.start(instance)
