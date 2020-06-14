# outpost

A little tool I made to reduce the cost of renting a VPS (Digital Ocean). This is heavily inspired by [pry0cc/axiom](https://github.com/pry0cc/axiom/), very cool tool! Whereas Axiom is for managing multiple different instances and has a lot of featutures, I created this to be a simple tool for managing just 1. It's not completely finished as I only drafted it up for personal use at the moment but it has very few dependancies and it makes it easy to quickly deploy a backed up VPS.

## Install
One line install
```
bash <(curl -s https://raw.githubusercontent.com/kr-b/outpost/master/tools/outpost-init)
```
At the moment, it uses a snapshot image called "outpost-snapshot", so if you want to use a specific VPS, shut it down and create a snapshot of it with that name and this tool should work out of the box.

## outpost-up
This creates a droplet from the saved snapshot image, then deletes the snapshot.

## outpost-ssh
This opens an ssh connection to the created VPS.

## outpost-pull / outpost-push
Uses `scp` to push or pull files to and from the server.

## outpost-down
This shuts down the server, creates a snapshot and deletes the droplet.