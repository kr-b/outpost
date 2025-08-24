# outpost/do_api.py
import os
import time
from pydo import Client

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DO_TOKEN")
client = Client(token=TOKEN)

def create_droplet(name, region, size):
    """Create droplet from most recent snapshot and return IP."""
    snapshots = client.snapshots.list(resource_type="droplet")
    if not snapshots["snapshots"]:
        raise Exception("No snapshots found. Run `outpost down` once to create one.")

    snapshot_id = snapshots["snapshots"][0]["id"]

    droplet = client.droplets.create({
        "name": name,
        "region": region,
        "size": size,
        "image": snapshot_id,
    })

    droplet_id = droplet["droplet"]["id"]

    # Poll until IP is assigned
    ip = None
    for _ in range(30):
        time.sleep(5)
        d = client.droplets.get(droplet_id)
        networks = d["droplet"]["networks"]["v4"]
        ipv4 = next((n for n in networks if n["type"] == "public"), None)
        if ipv4:
            ip = ipv4["ip_address"]
            break
    return ip

def destroy_droplet(name):
    """Snapshot and destroy droplet by name."""
    droplets = client.droplets.list()
    droplet = next((d for d in droplets["droplets"] if d["name"] == name), None)
    if not droplet:
        raise Exception(f"No droplet named {name} found.")

    droplet_id = droplet["id"]

    # Start snapshot
    action = client.droplet_actions.post(
        droplet_id,
        {"type": "snapshot", "name": f"{name}-backup"}
    )
    action_id = action["action"]["id"]

    # Poll action until completed
    while True:
        act = client.droplet_actions.get(droplet_id, action_id)
        status = act["action"]["status"]
        if status == "completed":
            print(f"Snapshot {name}-backup completed.")
            break
        elif status == "errored":
            raise Exception("Snapshot failed!")
        else:
            print(f"Snapshot in progress... (status={status})")
            time.sleep(10)

    # Now safe to destroy
    client.droplets.destroy(droplet_id=droplet_id)
    print(f"Droplet {name} destroyed, snapshot saved.")

def list_droplets():
    """List running droplets."""
    droplets = client.droplets.list()
    return [
        {
            "name": d["name"],
            "status": d["status"],
            "ip": next(
                (n["ip_address"] for n in d["networks"]["v4"] if n["type"] == "public"),
                None
            ),
        }
        for d in droplets["droplets"]
    ]

def get_droplet_ip(name):
    """Get IP address by droplet name."""
    droplets = client.droplets.list()
    droplet = next((d for d in droplets["droplets"] if d["name"] == name), None)
    if not droplet:
        return None
    networks = droplet["networks"]["v4"]
    ipv4 = next((n for n in networks if n["type"] == "public"), None)
    return ipv4["ip_address"] if ipv4 else None

def list_snapshots():
    """Return a list of droplet snapshots."""
    snaps = client.snapshots.list(resource_type="droplet")
    return [
        {"name": s["name"], "created_at": s["created_at"]}
        for s in snaps.get("snapshots", [])
    ]


def clear_snapshots(keep=1):
    """Delete old Outpost snapshots, keeping the latest N."""
    snaps = client.snapshots.list(resource_type="droplet")
    outpost_snaps = [
        s for s in snaps.get("snapshots", [])
        if s["name"].startswith("outpost")
    ]

    # Sort descending by creation date
    sorted_snaps = sorted(outpost_snaps, key=lambda s: s["created_at"], reverse=True)

    # Snapshots to delete: all except the latest `keep`
    to_delete = sorted_snaps[keep:]
    deleted_names = []

    for s in to_delete:
        client.snapshots.delete(s["id"])
        deleted_names.append(s["name"])

    return deleted_names
