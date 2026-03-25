Write-Host "A local bootstrap script is required to avoid committing secrets to git."
Write-Host "Copy deploy/bootstrap-personal-instances.example.ps1 -> deploy/bootstrap-personal-instances.local.ps1 and edit with your own email/password values."
Write-Host "Then run: .\\deploy\\bootstrap-personal-instances.local.ps1"

if (Test-Path "$PSScriptRoot\bootstrap-personal-instances.local.ps1") {
    Write-Host "Launching local bootstrap script..."
    . "$PSScriptRoot\bootstrap-personal-instances.local.ps1"
} else {
    Write-Host "Local file not found. Aborting."
    exit 1
}

$deployRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$instancesRoot = Join-Path $deployRoot "instances"

foreach ($instance in $instances) {
    $usrPath = Join-Path $instancesRoot "$($instance.Name)\usr"
    New-Item -ItemType Directory -Force -Path $usrPath | Out-Null

    $flaskSecret = ([Guid]::NewGuid().ToString("N") + [Guid]::NewGuid().ToString("N"))
    $envPath = Join-Path $usrPath ".env"

    @(
        "AUTH_LOGIN=$($instance.Login)"
        "AUTH_PASSWORD=$($instance.Password)"
        "FLASK_SECRET_KEY=$flaskSecret"
    ) | Set-Content -Path $envPath -Encoding ascii

    Write-Host ("Prepared {0} on port {1} at {2}" -f $instance.Name, $instance.Port, $usrPath)
}

Write-Host "Done. Start the stack with docker compose -f docker/run/docker-compose.yml up -d from the repo root."
