import click
from context import pass_context
from commands import *


@click.group(name='lfm')
@click.option('--topology',
              type=click.Path(exists=True, resolve_path=True),
              help='Topology File')
@click.option('--insecure',
              is_flag=True,
              help="Does not verify HTTPS connection")
@pass_context
def cli(ctx, topology=None, insecure=False):
    """Flow Manager CLI"""
    ctx.set_verify(not insecure)
    if topology is not None:
        ctx.set_topology(topology)

cli.add_command(cmd_path.path)
cli.add_command(cmd_eline.eline)
cli.add_command(cmd_treepath.treepath)
cli.add_command(cmd_etree.etree)
cli.add_command(cmd_tap.tap)
cli.add_command(cmd_ofnode.ofnode)

if __name__ == "__main__":
    cli()