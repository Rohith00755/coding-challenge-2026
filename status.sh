#!/usr/bin/env bash
PUSH_STATUS=$(gh api -H "Accept: application/vnd.github.v3.repository+json" \
  orgs/hackathon-2026-org/teams/participants/repos/hackathon-2026-org/coding-challenge-2026 \
  --jq '.permissions.push')

if [ "$PUSH_STATUS" = "true" ]; then
  echo "🟢 Submissions are OPEN (WRITE access enabled)"
else
  echo "🔒 Submissions are PAUSED (READ-ONLY access enabled)"
fi
