import click
from lfmcli.context import pass_context


@click.group()
def path():
    pass


@path.command(name='list')
@pass_context
def lst(ctx):
    fm = ctx.fm
    result = fm.get_paths()
    paths = result.get('paths')

    if paths is not None and len(paths) > 0:
        ctx.print_json(paths)
    else:
        click.echo("No paths found")


@path.command()
@click.argument('name', type=click.STRING)
@pass_context
def get(ctx, name):
    fm = ctx.fm
    result = fm.get_path(name)
    paths = [result.get('path')]

    if paths is not None and len(paths) > 0:
        ctx.print_json(paths)
    else:
        click.echo("Path {} not found".format(name))


@path.command()
@click.argument('name', type=click.STRING)
@click.argument('source-switch', type=click.STRING)
@click.argument('destination-switch', type=click.STRING)
@click.option('--waypoints',
              type=click.STRING,
              help="Waypoint",
              multiple=True)
@click.option('--provider',
              type=click.Choice(['sr', 'mpls']), default='sr')
@pass_context
def add(ctx, name, source_switch, destination_switch,
        waypoints=None, provider=None):
    fm = ctx.fm
    path = {
        'name': name,
        'endpoint1': { 'node': source_switch },
        'endpoint2': { 'node': destination_switch }
    }

    if provider:
        path['provider'] = provider

    # Constraints
    path['contraints'] = {}
    if waypoints:
        path['constraints']['waypoints'] = []
        order = 0
        for waypoint in waypoints:
            path['constraints']['waypoints'].append({
                'order': order,
                'nodeid': waypoint
            })
            order += 1

    result = fm.add_path(path=path)

    paths = result.get('paths')
    if paths is not None and len(paths) > 0:
        ctx.print_json(paths)
    else:
        click.echo("Path not added")


@path.command()
@pass_context
def purge(ctx):
    fm = ctx.fm
    result = fm.delete_paths()

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("Paths removed")
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("No Paths to remove")
    else:
        click.echo(result)
        click.echo("Cannot remove Paths")


@path.command()
@click.argument('name', type=click.STRING)
@pass_context
def delete(ctx, name):
    fm = ctx.fm
    result = fm.delete_path(name)

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("Path {} removed".format(name))
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("Path {} does not exists".format(name))
    else:
        click.echo(result)
        click.echo("Cannot remove Path {}".format(name))