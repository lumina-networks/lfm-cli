import click
from lfmcli.context import pass_context


@click.group()
def treepath():
    pass


@treepath.command(name='list')
@pass_context
def lst(ctx):
    fm = ctx.fm
    result = fm.get_treepaths()
    paths = result.get('treepaths')

    if paths is not None and len(paths) > 0:
        ctx.print_json(paths)
    else:
        click.echo("No Treepaths found")


@treepath.command()
@click.argument('name', type=click.STRING)
@pass_context
def get(ctx, name):
    fm = ctx.fm
    result = fm.get_treepath(name)
    paths = [result.get('treepaths')]

    if paths is not None and len(paths) > 0:
        ctx.print_json(paths)
    else:
        click.echo("Treepath {} not found".format(name))


@treepath.command()
@click.argument('name', type=click.STRING)
@click.argument('root-switch', type=click.STRING)
@click.argument('leaf-switch', type=click.STRING)
@click.option('--waypoints',
              type=click.STRING,
              help="Waypoint",
              multiple=True)
@click.option('--provider',
              type=click.Choice(['sr', 'mpls']), default='sr')
@pass_context
def add(ctx, self, name, root_switch,
        leaf_switch, waypoints=None, provider=None):
    fm = ctx.fm
    req = {
        'name': name,
        'root': {'node': root_switch},
        'leaves': {
            'leaf': [
                {
                    'node': leaf_switch,
                    'constraints': {}
                }
            ]
        }
    }

    if provider:
        req['provider'] = provider

    # Constraints
    if waypoints:
        constraints = req['leaves']['leaf'][0]['constraints']

        constraints['waypoints'] = []
        order = 0
        for waypoint in waypoints:
            constraints['waypoints'].append({
                'order': order,
                'nodeid': waypoint
            })
            order += 1

    result = fm.add_treepath(treepath=req)

    treepaths = result.get('treepaths')
    if treepaths is not None and len(treepaths) > 0:
        ctx.print_json(treepaths)
    else:
        click.echo("treepath not added")


@treepath.command()
@pass_context
def purge(ctx):
    fm = ctx.fm
    result = fm.delete_treepaths()

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("Treepaths removed")
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("No Treepaths to remove")
    else:
        click.echo(result)
        click.echo("Cannot remove Treepaths")


@treepath.command()
@click.argument('name', type=click.STRING)
@pass_context
def delete(ctx, name):
    fm = ctx.fm
    result = fm.delete_treepath(name)

    if 'status_code' in result and result['status_code'] == 200:
        click.echo("Treetpath {} removed".format(name))
    elif 'status_code' in result and result['status_code'] == 404:
        click.echo("Treetpath {} does not exists".format(name))
    else:
        click.echo(result)
        click.echo("Cannot remove Treetpath {}".format(name))