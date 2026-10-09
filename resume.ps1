$gh = if (Get-Command gh -ErrorAction SilentlyContinue) { "gh" } else { "C:\Program Files\GitHub CLI\gh.exe" }
& $gh api --method PUT -H "Accept: application/vnd.github+json" `
  orgs/hackathon-2026-org/teams/participants/repos/hackathon-2026-org/coding-challenge-2026 `
  -f permission='push'
Write-Host "🟢 Submissions RESUMED for coding-challenge-2026: WRITE access enabled." -ForegroundColor Green
