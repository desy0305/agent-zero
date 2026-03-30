# Personal Agent Zero Stack

This folder contains the shared-image, per-user deployment for the four isolated
Agent Zero containers.

## Quick start

1. Bootstrap the instance folders and initial auth files:

```powershell
powershell -ExecutionPolicy Bypass -File .\deploy\bootstrap-personal-instances.ps1
```

2. Start the stack from the repo root:

```powershell
docker compose -f docker\run\docker-compose.yml up -d
```

## Instances

- `sofiya` -> `http://localhost:50080`
- `valentina` -> `http://localhost:50081`
- `lazar` -> `http://localhost:50082`
- `vanya` -> `http://localhost:50083`

## Storage layout

- Shared image: `agent-zero-swarm:local`
- Per-user data: `C:\Users\adm20\Desktop\SERVER\a0\instances\<name>\usr`
- Per-user auth file: `C:\Users\adm20\Desktop\SERVER\a0\instances\<name>\usr\.env`

## Notes

- Only `/a0/usr` is mounted from the host.
- The application code stays inside the image layer, so the same image can be
  reused by all four containers.
- The initial password for all four users is `agent2026`. Each user can rotate
  it later in the GUI.
