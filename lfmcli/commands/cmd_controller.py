import click
from lfmcli.context import pass_context


@click.group()
def controller():
    pass


@controller.command(name='status')
@pass_context
def get_status(ctx):
    fm = ctx.fm
    result = fm.get_controller_status()
    system_status = result.get('content')

    if system_status is not None and len(system_status) > 0:
        ctx.print_json(system_status)
    else:
        click.echo("No system status found")

