# Offline-testable helpers; no network calls, authentication, or tenant writes.
Set-StrictMode -Version Latest
function Get-GraphFailureCategory {
 [CmdletBinding()] param([Parameter(Mandatory)][string]$Message)
 switch -Regex ($Message) {
  'empty string|UserId' { return 'MissingContextAccount' }
  '401|unauthorized|authentication' { return 'Authentication' }
  '403|forbidden|insufficient privileges' { return 'Authorization' }
  '429|throttl|too many requests' { return 'Throttling' }
  'timeout|timed out|network|DNS' { return 'Connectivity' }
  default { return 'Unclassified' }
 }
}
function ConvertTo-GraphDiagnosticSummary {
 [CmdletBinding()] param([AllowNull()][object]$Context,[AllowNull()][object]$Profile)
 $account = if($null -eq $Context){$null}else{$Context.Account}
 $tenant = if($null -eq $Context){$null}else{$Context.TenantId}
 $scopes = if($null -eq $Context){@()}else{@($Context.Scopes)}
 [pscustomobject]@{
  ContextAccountPresent = -not [string]::IsNullOrWhiteSpace([string]$account)
  ContextTenantPresent = -not [string]::IsNullOrWhiteSpace([string]$tenant)
  UserReadListed = $scopes -contains 'User.Read'
  ProfileRetrieved = ($null -ne $Profile -and -not [string]::IsNullOrWhiteSpace([string]$Profile.id))
  Assessment = if($null -ne $Profile -and $Profile.id){'GraphMeSucceeded'}else{'GraphMeNotVerified'}
 }
}
Export-ModuleMember -Function Get-GraphFailureCategory,ConvertTo-GraphDiagnosticSummary
