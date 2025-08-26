# outpost/cli.py
import click
from . import do_api

@click.group()
def cli():
    """Outpost - manage DigitalOcean droplets as remote hacking bases."""
    pass


@cli.command()
@click.option("--name", default="outpost", help="Droplet name")
@click.option("--region", default="fra1", help="Region slug (e.g. nyc3, sfo3)")
@click.option("--size", default="s-1vcpu-1gb", help="Droplet size")
def up(name, region, size):
    """Spin up a droplet from the latest snapshot."""
    ip = do_api.create_droplet(name, region, size)
    click.echo(f"Droplet {name} created at {ip}\nUse: ssh root@{ip}")


@cli.command()
@click.option("--name", default="outpost", help="Droplet name")
def down(name):
    """Snapshot and destroy a droplet."""
    do_api.destroy_droplet(name)


@cli.command()
def status():
    """List running droplets and available snapshots."""
    click.echo("=== Droplets ===")
    droplets = do_api.list_droplets()
    if not droplets:
        click.echo("No running droplets.")
    else:
        for d in droplets:
            click.echo(f"{d['name']} ({d['status']}) - {d['ip']}")

    click.echo("\n=== Snapshots ===")
    snapshots = do_api.list_snapshots()
    if not snapshots:
        click.echo("No snapshots found.")
    else:
        for s in snapshots:
            click.echo(f"{s['name']} ({s['created_at']})")


@cli.command()
@click.option("--keep", default=1, help="Number of latest snapshots to keep")
def clear(keep):
    """Delete old Outpost snapshots, keeping the most recent ones."""
    deleted = do_api.clear_snapshots(keep=keep)
    click.echo(f"Deleted snapshots: {', '.join(deleted) if deleted else 'None'}")

