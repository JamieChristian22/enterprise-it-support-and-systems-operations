BeforeAll {
 Import-Module "$PSScriptRoot/../scripts/GraphDiagnostics.Core.psm1" -Force
}
Describe 'Offline Graph diagnostic helper tests' {
 It 'recognizes missing context account' {
  Get-GraphFailureCategory -Message 'UserId because it is an empty string' | Should -Be 'MissingContextAccount'
 }
 It 'classifies authorization failures' {
  Get-GraphFailureCategory -Message '403 Forbidden' | Should -Be 'Authorization'
 }
 It 'classifies throttling' {
  Get-GraphFailureCategory -Message 'HTTP 429 Too Many Requests' | Should -Be 'Throttling'
 }
 It 'does not mistake absent context for success' {
  $r = ConvertTo-GraphDiagnosticSummary -Context $null -Profile $null
  $r.ContextAccountPresent | Should -BeFalse
  $r.ProfileRetrieved | Should -BeFalse
 }
 It 'distinguishes missing context from successful REST profile' {
  $r = ConvertTo-GraphDiagnosticSummary -Context ([pscustomobject]@{Account='';TenantId='';Scopes=@()}) -Profile @{id='synthetic-id'}
  $r.ContextAccountPresent | Should -BeFalse
  $r.ProfileRetrieved | Should -BeTrue
  $r.Assessment | Should -Be 'GraphMeSucceeded'
 }
 It 'reports a healthy synthetic context' {
  $r = ConvertTo-GraphDiagnosticSummary -Context ([pscustomobject]@{Account='test@example.invalid';TenantId='test';Scopes=@('User.Read')}) -Profile @{id='synthetic-id'}
  $r.ContextAccountPresent | Should -BeTrue
  $r.UserReadListed | Should -BeTrue
 }
}
