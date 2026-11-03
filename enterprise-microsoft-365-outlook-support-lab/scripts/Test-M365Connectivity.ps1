[CmdletBinding()]
param(
    [string]$OutputDirectory = "$env:USERPROFILE\Desktop"
)

$ErrorActionPreference = "Continue"
Import-Module (Join-Path $PSScriptRoot "modules\Support.Common.psm1") -Force

$outDir = New-SupportOutputDirectory -BasePath $OutputDirectory -Prefix "M365Connectivity"
$log = Join-Path $outDir "run.log"
$csv = Join-Path $outDir "connectivity-results.csv"

$targets = @(
    "outlook.office365.com",
    "login.microsoftonline.com",
    "office.com"
)

$results = foreach ($target in $targets) {
    Write-SupportLog -Message "Testing $target" -LogPath $log

    $dnsResolved = $false
    $addresses = ""
    try {
        $dns = Resolve-DnsName -Name $target -ErrorAction Stop
        $dnsResolved = $true
        $addresses = ($dns | Where-Object IPAddress | Select-Object -ExpandProperty IPAddress -Unique) -join ";"
    } catch {
        Write-SupportLog -Message "DNS resolution failed for $($target): $($_.Exception.Message)" -Level WARN -LogPath $log
    }

    $tcp = Test-NetConnection -ComputerName $target -Port 443 -WarningAction SilentlyContinue

    [pscustomobject]@{
        Timestamp      = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Target         = $target
        DnsResolved    = $dnsResolved
        IPAddresses    = $addresses
        Tcp443Success  = [bool]$tcp.TcpTestSucceeded
        RemoteAddress  = $tcp.RemoteAddress
        InterfaceAlias = $tcp.InterfaceAlias
        SourceAddress  = $tcp.SourceAddress
    }
}

$results | Export-Csv -Path $csv -NoTypeInformation -Encoding utf8
Write-SupportLog -Message "Connectivity report saved to $csv" -Level SUCCESS -LogPath $log
