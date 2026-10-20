param([Parameter(Mandatory=$true)][string]$ReferenceDirectory)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$taskRefs=(Resolve-Path -LiteralPath $ReferenceDirectory).Path
$taskCompiler=Join-Path $env:WINDIR 'Microsoft.NET\Framework\v4.0.30319\csc.exe'
$taskArgs=@('/nologo','/noconfig','/nostdlib+','/langversion:3','/platform:x86','/optimize+','/codepage:65001','/target:winexe',('/out:'+(Join-Path $taskRoot 'PeakMP3\PeakMP3.exe')),('/win32icon:'+(Join-Path $taskRoot 'PeakMP3\ASSETS\PeakMP3.ico')),('/win32manifest:'+(Join-Path $taskRoot 'PeakMP3\SOURCE\app.manifest')))
foreach($taskLibrary in @('mscorlib.dll','System.dll','System.Core.dll','System.Drawing.dll','System.Windows.Forms.dll')) {
 $taskPath=Join-Path $taskRefs $taskLibrary
 if(!(Test-Path -LiteralPath $taskPath)){throw ('Missing .NET3.5 reference: '+$taskLibrary)}
 $taskArgs+=('/r:'+$taskPath)
}
$taskSources=@(Get-ChildItem -LiteralPath (Join-Path $taskRoot 'PeakMP3\SOURCE') -Filter '*.cs' | ForEach-Object FullName)+@(Get-ChildItem -LiteralPath (Join-Path $taskRoot 'Shared') -Filter '*.cs' | ForEach-Object FullName)+@(Join-Path $taskRoot 'SOURCE\MiniJson.cs')
& $taskCompiler @taskArgs @taskSources
if($LASTEXITCODE -ne 0){throw 'PeakMP3 compilation failed'}
Write-Output 'Built PeakMP3 x86 CLR2 with .NET3.5 reference assemblies.'
