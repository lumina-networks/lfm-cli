import click
from lfmcli.context import pass_context


@click.group()
def eline():
    pass


@eline.command(name='list')
@pass_context
def lst(ctx):
    fm = ctx.fm
    result = fm.get_elines()
    elines = result.get('elines')

    if elines is not None and len(elines) > 0:
        ctx.print_json(elines)
    else:
        click.echo("No E-Lines Found")


@eline.command()
@click.argument('name', type=click.STRING)
@pass_context
def get(ctx, name):
    fm = ctx.fm
    result = fm.get_eline(name)
    elines = [result.get('eline')]

    if elines is not None and len(elines) > 0:
        ctx.print_json(elines)
    else:
        click.echo("E-Line {} not found".format(name))


@eline.command()
@click.argument('name', type=click.STRING)
def stats(ctx, name):
    fm = ctx.fm
    result = fm.get_eline_stats(name)

    stats = result.get('output')
    if stats is None:
        print("No E-Line stats found for {}".format(name))
    else:
        ctx.print_json(stats)


@eline.command()
@click.argument('name', type=click.STRING)
@click.argument('path-name', type=click.STRING)
@click.argument('source-port', type=click.STRING)
@click.argument('destination-port', type=click.STRING)
@click.option('--source-segmentation-id', type=click.INT, help="VLAN ID")
@click.option('--destination-segmentation-id', type=click.INT, help="VLAN ID")
@click.option('--ether-type', type=click.STRING, help="Ethernet Type")
@click.option('--bidirectional', type=click.BOOL, is_flag=True,
              help="Unidirectional/Bidirectional", default=True)
@click.option('--provider', type=click.Choice(['sr', 'mpls']), default='sr')
def add(ctx, name, path_name, source_port, destination_port,
              source_segmentation_id, destination_segmentation_id,
              ether_type, bidirectional, provider):
    fm = ctx.fm
    eline = {
        'name': name,
        'path-name': path_name,
        'endpoint1': {
                'switch-port': source_port
                },
        'endpoint2': {
            'switch-port': destination_port
            }
        }

    if source_segmentation_id:
            eline['endpoint1']['segmentation-id'] = \
                source_segmentation_id
            eline['endpoint1']['network-type'] = 'vlan'

    if destination_segmentation_id:
        eline['endpoint2']['segmentation-id'] = \
            destination_segmentation_id
        eline['endpoint2']['network-type'] = 'vlan'

    if ether_type:
        eline['ethernet-type'] = ether_type

    if provider:
        eline['provider'] = provider

    if bidirectional:
        eline['bidirectional'] = 'true'

    result = fm.add_eline(eline=eline)

    elines = result.get('elines')
    if elines is not None and len(elines) > 0:
        ctx.print_json(elines)
    else:
        click.echo("E-Line Not Added")


@eline.command()
def purge(ctx):
    fm = ctx.fm
    result = fm.delete_elines()

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("All E-Lines removed")
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("No E-Lines to remove")
    else:
        click.echo(result)
        click.echo("Cannot remove E-Lines")


@eline.command()
@click.argument('name', type=click.STRING)
def delete(ctx, name):
    fm = ctx.fm
    result = fm.delete_eline(name)

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("E-Line {} removed".format(name))
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("E-line {} does not exist".format(name))
    else:
        click.echo(result)
        click.echo("Cannot remove E-Line {}".format(name))