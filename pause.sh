#!/usr/bin/env bash
gh api --method PUT -H "Accept: application/vnd.github+json" \
  orgs/hackathon-2026-org/teams/participants/repos/hackathon-2026-org/coding-challenge-2026 \
  -f permission='pull'
echo "🔒 Submissions PAUSED for coding-challenge-2026: Team set to READ-ONLY."
