# Owner Action Checklist

Date: 2026-02-20  
Project: us_stock_ver2

This checklist tracks what is automated in-repo and what still requires owner action in GitHub/GitLab UI.

## 1) Remote Repository And Push Permission

Automated status:
- Local repository is ready.
- `main` branch exists.
- No `origin` remote is configured yet.

Owner action needed:
- Create remote repository (`us_stock_ver2`) in GitHub or GitLab.
- Ensure your account has push permission.
- Configure auth with PAT or SSH key.

Commands to run locally:
```powershell
git remote add origin <REMOTE_URL>
git add .
git commit -m "chore: initialize repo with CI and operations policy"
git push -u origin main
```

Verification:
- Push completes without auth/permission error.

## 2) CI Platform Permissions

Automated status:
- CI workflows are added:
  - `.github/workflows/ci.yml`
  - `.github/workflows/secrets-and-boot-check.yml`

Owner action needed (GitHub):
- Repository Settings -> Actions -> General:
  - Enable Actions for this repository.
  - Allow workflow run permissions for your account/role.

Verification:
```powershell
git commit --allow-empty -m "chore: trigger ci"
git push
```
- Confirm CI starts automatically in Actions tab.

## 3) Production Secret Issuance And Registration

Automated status:
- Required secret validator script added: `backend/scripts/validate_required_env.py`
- Manual workflow added to validate secrets + boot app:
  - `.github/workflows/secrets-and-boot-check.yml`

Owner action needed:
- Issue and register real values for:
  - `GEMINI_API_KEY`
  - `FRED_API_KEY`
  - `FINNHUB_API_KEY`
  - `FMP_API_KEY`
  - `DATABASE_URL`
  - `REDIS_URL`

Verification:
- In GitHub Actions, run `Secrets And Boot Check` for `staging` and `production`.
- Workflow should pass in both environments.

## 4) Final Operations Policy Values

Automated status:
- Draft with concrete numeric thresholds added:
  - `docs/operations/OPERATIONS_POLICY_v1.md`

Owner action needed:
- Review and approve numeric thresholds.
- Fill owner approval fields in the policy document.

## 5) Deployment Approval Model

Automated status:
- Deployment governance draft added:
  - `docs/operations/DEPLOYMENT_APPROVAL_v1.md`

Owner action needed:
- Fill approver GitHub IDs.
- Confirm deploy window and rollback criteria.
- Approve document revision.
