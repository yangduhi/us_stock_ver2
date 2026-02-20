# Deployment Approval And Rollback Policy v1

Version: 1.0  
Date: 2026-02-20  
Status: Draft for Owner Approval

## 1) Approvers

Required approvers for production deploy:
- Primary approver: Repository owner (`TBD_GITHUB_ID`)
- Secondary approver (backup): (`TBD_GITHUB_ID`)

Rule:
- At least one required approver must explicitly approve each production release.

## 2) Deployment Windows

Default production deploy window (US/Eastern):
- Monday to Thursday: `09:30 - 16:00`
- Friday: `09:30 - 14:00`

Out-of-window deploy:
- Allowed only for hotfix/security incidents with explicit emergency approval.

## 3) Pre-Deploy Gate

Before production deploy, all must pass:
- Latest `CI` workflow is green.
- `Secrets And Boot Check` passes for `production` environment.
- No open critical incident.
- Release note includes rollback command/path.

## 4) Rollback Triggers

Rollback immediately if one or more are true:
- API error rate `> 5.0%` for 10 minutes post-deploy.
- `p95 > 3.0s` for 15 minutes post-deploy.
- Boot failure or repeated crash loop.
- Data correctness issue with financial output.

## 5) Rollback Procedure

Minimum required actions:
1. Announce rollback in incident channel with timestamp.
2. Revert to last known good release/tag.
3. Validate `/health` and root endpoint.
4. Confirm recovery metrics for at least 15 minutes.
5. Publish post-incident summary.

## Approval

- Final approver list confirmed by: `TBD`
- Effective date: `TBD`
- Review date (next): `2026-03-20`
