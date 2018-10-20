import click
from lfmcli.context import pass_context


@click.group()
def ofnode():
    pass


@ofnode.command(name='list')
@pass_context
def lst(ctx):
    fm = ctx.fm
    result = fm.get_ofnodes()
    nodes = result.get('nodes')

    if nodes is not None and len(nodes) > 0:
        ctx.print_json(nodes)
    else:
        click.echo("No OF Nodes Found")


@ofnode.command()
@click.argument('node', type=click.STRING)
@pass_context
def get(ctx, node):
    fm = ctx.fm
    result = fm.get_ofnode(node)
    nodes = [result.get('node')]
    if nodes is not None and len(nodes) > 0:
        ctx.print_json(nodes)
    else:
        click.echo("OF node {} not found".format(node))