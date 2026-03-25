# Agent Zero + Agent Zero Swarm: Local Multi-Agent Deployment

This guide covers the most reliable approach to run `agent-zero` and `agent-zero-swarm` together with Docker Compose, including Docker-in-Docker CLI and MCP compatibility. The configuration is designed for reproducible local setups and secure host Docker socket usage.

## 1. Prerequisites

- Docker Engine installed on host
- Docker Compose (v2 or v1) available
- Local clone of `agent-zero` repo. If you cloned `agent-zero-swarm` separately, keep it as part of your local working tree:

```bash
cd ~/projects/agent-zero
# ensure agent-zero-swarm location known, e.g. ../agent-zero-swarm
```

## 2. Build a custom image with Docker CLI baked in

In `agent-zero/DockerfileLocal` we install docker CLI:

```dockerfile
FROM agent0ai/agent-zero-base:latest
ARG BRANCH=local
ENV BRANCH=$BRANCH
USER root
RUN apt-get update && apt-get install -y docker.io && rm -rf /var/lib/apt/lists/*
# rest of pipeline as existing
```

## 3. Update Compose for socket mount + DOCKER_HOST

In `docker/run/docker-compose.yml`, ensure each service has:

- `- /var/run/docker.sock:/var/run/docker.sock`
- `- DOCKER_HOST=unix:///var/run/docker.sock`

This allows all agents to control host Docker from inside container.

## 4. Example Compose for multi-instance

A new file `docker/run/docker-compose.example.yml` already includes this pattern.

### 5. Add run instructions

```bash
docker compose -f docker/run/docker-compose.yml up -d
# or compose.example if you copy it
```

## 5. Optional: Integrate `agent-zero-swarm`

If you want an integrated approach, you can keep `agent-zero-swarm` repo as part of your local tree and use a compose service from there:

- In `agent-zero/docker/run/docker-compose.yml`, keep `image: agent-zero-swarm:local` and `build` pointing to `../..`, which may reference the swarm Dockerfile in the combined repo.
- Use same `ssh` & `ports` routing as in this repo.

## 6. Version control notes

- This guide is set up for local private workflows.
- To push to your fork, add remote and push:

```bash
git remote add fork https://github.com/desy0305/agent-zero.git
git push -u fork main
```

- Keep the `agent-zero-swarm` code on a sibling repo, or include it in your own fork if desired.

## 7. Troubleshooting

- `docker` command not found: rebuild `DockerfileLocal` after edits.
- Socket access errors: verify host path and run `chmod 666 /var/run/docker.sock` (or better, add to docker group in host).
- `agent-zero-swarm` failure: ensure `docker-compose.yml` service names are consistent and the `agent-zero-swarm` image is built from local context.
