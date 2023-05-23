param(
    [Parameter(Mandatory=$true)]
    [string]$projectName,
    [string]$basePath
)

if ($basePath -eq "") {
    $basePath = "E:\Programming\git"
}

$projectDir = "$basePath\$projectName"
$initialDir = $PWD

Write-Host "Moving to project dir $projectDir"
cd $projectDir

$command = dotnet build
Write-Host "Executing command '$command'"
$command

$response = $LASTEXITCODE

if (!$response -eq 0) {
    exit -1
}

Write-Host "Returning to initial working dir $initialDir"
cd $initialDir

exit 0