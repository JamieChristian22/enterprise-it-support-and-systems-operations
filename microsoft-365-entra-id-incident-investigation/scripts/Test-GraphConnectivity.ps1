#Requires -Version 7.0
<#
.SYNOPSIS
Read-only delegated Microsoft Graph /me connectivity diagnostic.
.DESCRIPTION
Does not write directory data. Prompts for delegated User.Read only if no context is available.
#>
[CmdletBinding()]
param([switch]$Connect)
$ErrorActionPreference = 'Stop'
try {
    if (-not (Get-Module -ListAvailable Microsoft.Graph.Authentication)) {
        throw 'Microsoft.Graph.Authentication module missing. Install-Module Microsoft.Graph -Scope CurrentUser'
    }
    Import-Module Microsoft.Graph.Authentication -ErrorAction Stop
    if ($Connect) { Connect-MgGraph -Scopes 'User.Read' -NoWelcome -ErrorAction Stop }
    Write-Host 'Checking Microsoft Graph delegated /me endpoint (read-only)...'
    $profile = Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/me' -ErrorAction Stop
    if (-not $profile.id) { throw 'Response did not contain a user id.' }
    [pscustomobject]@{
        Result = 'PASS'
        DisplayName = $profile.displayName
        UserPrincipalName = $profile.userPrincipalName
        Endpoint = '/v1.0/me'
        CheckedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    } | Format-List
    Write-Host 'Do not publish identifying output without redaction.'
} catch {
    Write-Error "Graph /me check failed: $($_.Exception.Message)"
    exit 1
}
