param(
    [Parameter(Mandatory = $true)]
    [string]$projectName,
    [Parameter(Mandatory = $true)]
    [string]$out,
    [string]$subProject,
    [string]$netVersion,
    [string]$basePath,
    [string]$buildMode
)

function Get-Files
{
    param(
        [Parameter(Mandatory = $true)] $fileDir,
        [Parameter(Mandatory = $true)] $filter)

    Write-Host "Searching for $filter files in $fileDir"
    $files = (Get-ChildItem -Path $fileDir -Filter $filter).FullName

    if (($files -isnot [system.array]) -and ($files -isnot [system.string]))
    {
        Write-Host "Did not find any dlls in $fileDir"
        exit -1
    }

    if ($files -is [system.array])
    {
        return $files
    }

    return @($files)
}

function Get-SingleSubDirRecursive
{
    param(
        [Parameter(Mandatory = $true)] $baseDir,
        [Parameter(Mandatory = $true)] $filter)

    Write-Host "Searching for '$filter' dir in $baseDir"

    # Get-ChildItem -Path $projectDir -Filter $filter -Recurse -ErrorAction SilentlyContinue -Force
    $subDir = (Get-ChildItem -r -Path $baseDir -Filter $filter -Directory).Fullname

    if (($subDir -isnot [system.string]) -or $subDir -eq "")
    {
        Write-Host $subDir
        Write-Host "Could not find a obvious '$filter' directory in $baseDir"
        exit -1
    }
    return $subDir
}

if ($basePath -eq "")
{
    $basePath = "E:\Programming\git"
}

if ($netVersion -eq "")
{
    $netVersion = "net7.0"
}

if ($buildMode -eq "")
{
    $buildMode = "Release"
}

$projectDir = "$basePath\$projectName"

if (!$subProject -eq "")
{
    $projectDir = Get-SingleSubDirRecursive -baseDir $projectDir -filter "$subProject"
}

$binDir = Get-SingleSubDirRecursive -baseDir $projectDir -filter "bin"
$binDir = Get-SingleSubDirRecursive -baseDir $binDir -filter "$buildMode"
$binDir = Get-SingleSubDirRecursive -baseDir $binDir -filter "*$netVersion*"

$dlls = Get-Files -fileDir $binDir -filter *.dll
$xmls = Get-Files -fileDir $binDir -filter *.xml

$copyFiles = $dlls + $xmls
Write-Host $copyFiles

Write-Host "Files found:"
foreach ($file in $copyFiles)
{
    Write-Host $file
}

Write-Host "Copying files"
Copy-Item -Path $copyFiles -Destination $out
if (!$LASTEXITCODE -eq 0)
{
    Write-Host "Failed to copy .dll file $copyFiles"
    exit -1
}

Write-Host "Done"
exit 0