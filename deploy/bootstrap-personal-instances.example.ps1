# Copy this file to bootstrap-personal-instances.local.ps1 and edit it with your own credentials.
# Do not commit local credentials to git.

$ErrorActionPreference = "Stop"

$instances = @(
    @{ Name = "sofiya"; Login = "sofiya@example.com"; Password = "YourSecurePassword1"; Port = 50080 },
    @{ Name = "valentina"; Login = "valentina@example.com"; Password = "YourSecurePassword2"; Port = 50081 },
    @{ Name = "lazar"; Login = "lazar@example.com"; Password = "YourSecurePassword3"; Port = 50082 },
    @{ Name = "vanya"; Login = "vanya@example.com"; Password = "YourSecurePassword4"; Port = 50083 }
)

$deployRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$instancesRoot = Join-Path $deployRoot "instances"

foreach ($instance in $instances) {
    $usrPath = Join-Path $instancesRoot "$($instance.Name)\usr"
    New-Item -ItemType Directory -Force -Path $usrPath | Out-Null

    $flaskSecret = ([Guid]::NewGuid().ToString("N") + [Guid]::NewGuid().ToString("N"))
    $envPath = Join-Path $usrPath ".env"

    @(
        "AUTH_LOGIN=$($instance.Login)",
        "AUTH_PASSWORD=$($instance.Password)",
        "FLASK_SECRET_KEY=$flaskSecret"
    ) | Set-Content -Path $envPath -Encoding ascii

    Write-Host ("Prepared {0} on port {1} at {2}" -f $instance.Name, $instance.Port, $usrPath)
}

Write-Host "Done. Start the stack with docker compose -f docker/run/docker-compose.yml up -d from the repo root."
