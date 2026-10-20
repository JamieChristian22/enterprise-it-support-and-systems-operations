#Requires -Version 7.0
<#
.SYNOPSIS
Read-only self-profile and Graph SDK context diagnostics.
.NOTES
No changes to users, roles, licenses, Conditional Access or sessions.
Use an authorized account and redact terminal output before sharing.
#>
[CmdletBinding()]
param([switch]$Connect)
$ErrorActionPreference = 'Stop'
try {
    Import-Module Microsoft.Graph.Authentication -ErrorAction Stop
    if ($Connect) { Connect-MgGraph -Scopes 'User.Read' -NoWelcome -ErrorAction Stop }
    $ctx = Get-MgContext
    if ($null -eq $ctx) { Write-Warning 'Graph context is null; attempting /me independently.' }
    else {
        [pscustomobject]@{
            ContextAccountPresent = -not [string]::IsNullOrWhiteSpace($ctx.Account)
            ContextTenantPresent = -not [string]::IsNullOrWhiteSpace($ctx.TenantId)
            UserReadListed = @($ctx.Scopes) -contains 'User.Read'
            AuthType = $ctx.AuthType
        } | Format-List
    }
    $me = Invoke-MgGraphRequest -Method GET -Uri 'https://graph.microsoft.com/v1.0/me' -ErrorAction Stop
    if (-not $me.id) { throw 'Graph /me response missing id.' }
    [pscustomobject]@{
        ProfileRetrieved = $true
        DisplayName = $me.displayName
        UserPrincipalName = $me.userPrincipalName
        Source = 'GET /v1.0/me'
        CheckedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    } | Format-List
    Write-Host 'Result: successful self-profile query. No directory data changed.'
} catch {
    Write-Error "Read-only diagnostic failed: $($_.Exception.Message)"
    exit 1
}
