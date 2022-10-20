import click

from gravity import options
from gravity import process_manager


@click.command("exec")
@click.option("--no-exec", "-n", is_flag=True, default=False, help="Don't exec, just print the command that would be run")
@options.instances_services_arg()
@click.pass_context
def cli(ctx, instances_services, no_exec):
    """Run a single Galaxy service in the foreground, with logging output to stdout/stderr.

    Zero or one instance names can be provided in INSTANCES, it is required if more than one Galaxy instance is
    configured in Gravity.

    Exactly one service name is required in SERVICES.
    """
    with process_manager.process_manager(**ctx.parent.cm_kwargs) as pm:
        pm.exec(instance_names=instances_services, no_exec=no_exec)
