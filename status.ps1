$gh = if (Get-Command gh -ErrorAction SilentlyContinue) { "gh" } else { "C:\Program Files\GitHub CLI\gh.exe" }
$pushStatus = & $gh api -H "Accept: application/vnd.github.v3.repository+json" `
  orgs/hackathon-2026-org/teams/participants/repos/hackathon-2026-org/coding-challenge-2026 `
  --jq ".permissions.push"

if ($pushStatus -eq "true") {
  Write-Host "🟢 Submissions are OPEN (WRITE access enabled)" -ForegroundColor Green
} else {
  Write-Host "🔒 Submissions are PAUSED (READ-ONLY access enabled)" -ForegroundColor Yellow
}
