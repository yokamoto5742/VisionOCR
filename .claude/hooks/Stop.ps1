#Requires -Version 5.0
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

try {
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
    [System.Windows.Forms.MessageBox]::Show("作業が完了しました", 'Claude Code', [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information) | Out-Null
}
catch {
    Write-Output "Hook failed: $_"
}