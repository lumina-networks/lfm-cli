import click
from lfmcli.context import pass_context


@click.group()
def tap():
    pass


@tap.command()
@click.argument('eline-name', type=click.STRING)
@click.argument('endpoint', type=click.STRING)
@pass_context
def get(ctx, eline_name, endpoint):
    fm = ctx.fm
    result = fm.get_taps(eline_name, endpoint)

    taps = result.get(endpoint)
    if taps is not None and len(taps) > 0:
        ctx.print_json(taps)
    else:
        click.echo("no taps found")


@tap.command()
@click.argument('eline-name', type=click.STRING)
@click.argument('endpoint', type=click.STRING)
@click.argument('path-name', type=click.STRING)
@click.argument('output-port', type=click.STRING)
@pass_context
def add(ctx, eline_name, endpoint, path_name, output_port):
    fm = ctx.fm
    tap = {
        'path-name': path_name,
        'egress': {
            'action': [
                {
                    'order': 3,
                    'output-action': {
                        'output-node-connector': output_port
                    }
                }
            ]
        }
    }

    result = fm.add_tap(eline_name, endpoint, tap=tap)

    taps = result.get('taps')
    if taps is not None and len(taps) > 0:
        ctx.print_json(taps)
    else:
        click.echo("Tap not added: {}".format(result.get('content')))


@tap.command()
@click.argument('eline-name', type=click.STRING)
@click.argument('endpoint', type=click.STRING)
@pass_context
def purge(ctx, eline_name, endpoint):
    fm = ctx.fm
    result = fm.delete_taps(eline_name, endpoint)

    if 'status_code' in result and result['status_code'] == 200:
        click.echo(
            "All Taps removed for {} on {}".format(eline_name, endpoint))
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo(
            "No Taps to remove for {} on {}".format(eline_name, endpoint))
    else:
        click.echo(result)
        click.echo(
            "Cannot remove Taps for {} on {}".format(eline_name, endpoint))


@tap.command()
@click.argument('eline-name', type=click.STRING)
@click.argument('endpoint', type=click.STRING)
@click.option('path-name', type=click.STRING)
@pass_context
def delete(ctx, eline_name, endpoint, path_name):
    fm = ctx.fm
    result = fm.delete_tap(eline_name, endpoint, path_name)
    tap_name = '{}/{}/{}'.format(eline_name, endpoint, path_name)

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("Tap {} removed for {} on {}".format(tap_name,
                                                        eline_name,
                                                        endpoint))
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("Tap {} does not exist for {} on {}".format(tap_name,
                                                               eline_name,
                                                               endpoint))
    else:
        click.echo(result)
        click.echo("Cannot remove Tap {} for {} on {}".format(tap_name,
                                                              eline_name,
                                                              endpoint))