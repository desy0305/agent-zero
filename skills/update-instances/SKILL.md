---
name: Mass Update All Instances
description: Pulls the latest code from the custom fork on GitHub, rebuilds the Docker image, and restarts all active Agent Zero instances.
---

# Mass Update All Instances

This skill automates the process of fetching the latest updates from your fork and applying them across all running instances by triggering a Docker Compose rebuild.

## How it works
1. It validates access to the host's Docker socket.
2. It fetches your latest remote `fork/main` branch locally.
3. It uses `docker compose` to build the new `agent-zero-swarm:local` image.
4. It restarts the containers defined in the current deployment.

> **Note to Agent**: To execute this mass update, run the provided script exactly as written. Because this rebuilds the image the agent itself is running in, the final step will temporarily disconnect the user interface while the cluster comes back up.

## Command to execute update

The agent should run the following commands sequentially in the terminal tool:

```bash
# Ensure we are in the main repository
cd /git/agent-zero || exit 1

# Add the user's fork remote if it doesn't already exist
git remote add fork https://github.com/desy0305/agent-zero.git || true

# Fetch the latest tags and main branch from the fork
git fetch fork
git fetch fork --tags

# Reset the working tree to the latest fork main branch
git reset --hard fork/main

# Build the base docker container and restart all services
echo "Beginning mass update and container rebuild. System will reboot..."
docker compose -f docker/run/docker-compose.yml build
docker compose -f docker/run/docker-compose.yml up -d
```

> **Important Constraint**: Do NOT push or commit anything to the public `agent0ai` source repo. The update MUST only pull from the `fork` remote.
