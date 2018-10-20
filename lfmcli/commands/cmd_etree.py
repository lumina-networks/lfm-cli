import click
from lfmcli.context import pass_context

@click.group()
def etree():
    pass

@etree.command(name='list')
@pass_context
def lst(ctx):
    fm = ctx.fm
    result = fm.get_etrees()
    etrees = result.get('etrees')

    if etrees is not None and len(etrees) > 0:
        ctx.print_json(etrees)
    else:
        click.echo("No E-Trees Found")

@etree.command()
@click.argument('name', type=click.STRING)
@pass_context
def get(ctx, name):
    fm = ctx.fm
    result = fm.get_etree(name)
    etrees = [result.get('etree')]

    if etrees is not None and len(etrees) > 0:
        ctx.print_json(etrees)
    else:
        click.echo("E-Tree {} not found".format(name))


@etree.command()
@click.argument('name', type=click.STRING)
@pass_context
def stats(ctx, name):
    fm = ctx.fm
    result = fm.get_etree_stats(name)

    stats = result.get('output')
    if stats is None:
        print("No E-Tree stats found for {}".format(name))
    else:
        ctx.print_json(stats)


@etree.command()
@click.argument('name', type=click.STRING)
@click.argument('path-name', type=click.STRING)
@click.argument('root-port', type=click.STRING)
@click.argument('leaf-port', type=click.STRING)
@click.option('--root-segmentation-id', type=click.INT, help="VLAN ID")
@click.option('--leaf-segmentation-id', type=click.INT, help="VLAN ID")
@click.option('--ether-type', type=click.STRING, help="Ether type")
@click.option('--provider', type=click.Choice(['sr', 'mpls']), default='sr')
@pass_context
def add(ctx, name, path_name, root_port, leaf_port,
              root_segmentation_id, leaf_segmentation_id,
              ether_type, provider):
    fm = ctx.fm
    etree = {
        'name': name,
        'path-name': path_name,
        'root': {
            'switch-port': root_port
        },
        'leaves': [
            {
                'leaf': {
                    'switch-port': leaf_port
                }
            }
        ]
    }

    if root_segmentation_id:
        etree['root']['segmentation-id'] = root_segmentation_id
        etree['root']['network-type'] = 'vlan'

    if leaf_segmentation_id:
        etree['leaf']['segmentation-id'] = leaf_segmentation_id
        etree['leaf']['network-type'] = 'vlan'

    if ether_type:
        etree['ethernet-type'] = ether_type

    if provider:
        etree['provider'] = provider

    result = fm.add_etree(etree=etree)

    etrees = result.get('etrees')
    if etrees is not None and len(etrees) > 0:
        ctx.print_json(etrees)
    else:
        print "E-Tree not added"


@etree.command()
@pass_context
def purge(ctx):
    fm = ctx.fm
    result = fm.delete_etrees()

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("E-Trees removed")
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("No E-Trees to remove")
    else:
        click.echo(result)
        click.echo("Cannot remove E-Trees")

@etree.command()
@click.argument('name', type=click.STRING)
@pass_context
def delete(ctx, name):
    fm = ctx.fm
    result = fm.delete_etree(name)

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("E-Tree {} removed".format(name))
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("E-Tree {} does not exist".format(name))
    else:
        click.echo(result)
        click.echo("Cannot remove E-Trees {}".format(name))