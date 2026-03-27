param(
    [string]$ImageName = "student-feedback-app:latest",
    [string]$ContainerName = "student-feedback-app",
    [string]$HostPort = "5000",
    [string]$ContainerPort = "5000"
)

$ErrorActionPreference = "Stop"

$playbookExtraVars = "image_name=$ImageName container_name=$ContainerName host_port=$HostPort container_port=$ContainerPort"

$ansiblePlaybookCmd = Get-Command ansible-playbook -ErrorAction SilentlyContinue
if ($ansiblePlaybookCmd) {
    Write-Host "Using host ansible-playbook..."
    ansible-playbook -i ansible/inventory ansible/deploy.yml --extra-vars $playbookExtraVars
    exit $LASTEXITCODE
}

Write-Host "Host ansible-playbook not found. Using containerized Ansible..."
$dockerCmd = @(
    "run", "--rm",
    "-v", "${PWD}:/workspace",
    "-w", "/workspace",
    "-v", "/var/run/docker.sock:/var/run/docker.sock",
    "cytopia/ansible:latest",
    "sh", "-lc",
    "/opt/venv/bin/pip install --quiet requests docker && /opt/venv/bin/ansible-playbook -i ansible/inventory ansible/deploy.yml -e ansible_python_interpreter=/opt/venv/bin/python --extra-vars '$playbookExtraVars'"
)

& docker @dockerCmd
exit $LASTEXITCODE
