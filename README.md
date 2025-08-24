# Outpost

Outpost is a Python CLI tool to manage ephemeral DigitalOcean droplets as remote hacking bases.
Spin up droplets from your snapshots, run them when needed, and spin them down to avoid unnecessary charges. Perfect for bug bounty or CTF work from lightweight devices like an iPad.

---

## Features

* **Spin up droplets** from the latest Outpost snapshot
* **Spin down droplets** with automatic snapshot backup
* **List status** of running droplets and available snapshots
* **SSH** into droplets quickly from the CLI
* **Clear old snapshots** to keep your account tidy
* Filters only Outpost-created snapshots, avoiding random snapshots

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kr-b/outpost.git
cd outpost
```

2. Install in editable mode:

```bash
pip install -e .
```

3. Set your DigitalOcean API token:

```bash
export DO_TOKEN="your_digitalocean_api_token"
```

---

## Usage

### Spin up a droplet

```bash
outpost up --name lab --region nyc3 --size s-1vcpu-1gb
```

### Spin down a droplet (creates snapshot first)

```bash
outpost down --name lab
```

### List status

```bash
outpost status
```

Shows running droplets and available Outpost snapshots.

### SSH into a droplet

```bash
outpost ssh --name lab
```

### Clear old snapshots

```bash
outpost clear --keep 1
```

Deletes old Outpost snapshots, keeping only the most recent N (default 1).

---

## Configuration

Outpost reads your DigitalOcean API token from the `DO_TOKEN` environment variable.

Optional CLI parameters:

* `--name` — droplet name (default: `outpost`)
* `--region` — droplet region (default: `nyc3`)
* `--size` — droplet size (default: `s-1vcpu-1gb`)
* `--keep` — number of snapshots to keep when clearing
