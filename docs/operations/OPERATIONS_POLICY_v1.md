# Operations Policy v1

Version: 1.0  
Date: 2026-02-20  
Status: Draft for Owner Approval

## Scope

This policy defines production SLO thresholds, paging criteria, and fallback allowances for `us_stock_ver2`.

## 1) SLO Thresholds

Measurement window:
- Rolling 30 days for SLO compliance
- Rolling 5/10/15 minutes for alerts

Service level objectives:
- Availability: `>= 99.5%` monthly
- API error rate (5xx + unhandled exceptions): `<= 1.0%` over 5-minute window
- API latency:
  - `p95 <= 2.0s` for `/api/v1/dashboard/overview`
  - `p95 <= 2.0s` for `/api/v1/market/tickers/{ticker}/analysis`

## 2) Alerting And Paging Criteria

Non-page alert (Slack/ChatOps):
- Error rate `> 2.0%` for 15 minutes
- `p95 > 2.5s` for 15 minutes

Page immediately (on-call):
- Availability `< 99.0%` over 10 minutes
- Error rate `> 5.0%` for 10 minutes
- `p95 > 3.0s` for 15 minutes
- Any boot failure after deployment

## 3) Fallback Policy

Allowed:
- Neutral fallback (`value=50`, `label=Neutral`) is allowed only when upstream data source is unavailable.
- Response must include warning metadata (for example `warning` or equivalent).

Not allowed:
- Silent fallback without warning metadata.
- Forced numeric zero fallback (`0`) for analytics scores in production.

Guardrail:
- If fallback responses exceed `10%` of requests for 10 minutes on a critical endpoint, trigger page.

## 4) Review Cadence

- Review monthly or after major incident.
- Any threshold change requires version bump and owner approval.

## Approval

- Owner (name/id): `TBD`
- Approved date: `TBD`
- Signature/record link: `TBD`
