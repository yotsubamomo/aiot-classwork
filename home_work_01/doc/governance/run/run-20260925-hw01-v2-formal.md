# Run record — HW01 Weather Map V2 Formal implementation run (`home_work_01/`)

Orchestrator run-to-completion record (orch-default §12; Bindings §7). Control-plane authority only (governance §2.1 Orchestrator row). This file is a `doc/governance/**` record-only path (Bindings §7; orch-default §7 P7).

## Run identity

| Field | Value |
| --- | --- |
| Run id | `run-20260925-hw01-v2-formal` |
| Started | 2026-09-25 |
| Lane | Formal (Bindings §4: 作業主體) — Delta Spec + Tickets + Orchestrator, parallelism 1 (Bindings §6) |
| Outcome Contract | `home_work_01/doc/governance/outcome-contract-v2.md` — **ACCEPTED 2026-09-25** (§9); acceptor verbatim record §9.1; normative candidate `69c5a049104b2fd96289d10ff938c2c8a6d59bd4` |
| Derived contracts | `home_work_01/doc/spec/SPEC-V2.md` **v2.2** DERIVED (以參照繼承 V1 Spec v1.1; derivation `decisions/derivation-SPEC-V2.md`); Tickets **#35–#41** (GitHub Issues) |
| Bindings version | **b3** (2026-09-25) |
| Governance | Minimal Operational Governance v2.0; impl-default v2; orch-default v2; Model Profile default v2.2 (`executor` override b2 → opus-5-5) |

## Activation

- **Designation**: acceptor (GitHub `yotsubamomo`) 2026-09-25 activation prompt — "You are the Orchestrator for the HW01 Weather Map V2 Formal run … Begin the authorized run." Execute the authorized V2 Ticket set #35→#41 in dependency order, run autonomously; stop only for genuine boundaries. Designation ≠ Outcome Contract acceptance (orch-default §3; governance §1.2) — the acceptance authority is the OC-V2 §9.1 record.
- **Standing authorization for the run** (governance §1.2; unattended-run policy `decisions/decision-20260924-unattended-run-policy.md`, applicable per OC-V2 §6): accepted OC-V2 + effective SPEC-V2 v2.2 + Ticket graph + governance as standing authorization for work inside the accepted boundary. **SA-1** (topic-branch commit/push), **SA-2** (open PR). Reserved: **RB-1** merge, **RB-2** submission, **RB-3** (Vercel credential entry / third-party account ops; A-3 local read-only `.env` is authorized), **RB-4** payment, **RB-5** (outside authorized `home_work_01` workflow scope / files outside the unit), **RB-6** destructive git.
- **Credential boundary**: local untracked `.env` usable only under the already-authorized **A-3** boundary (bounded, read-only GET, no polling/load-test, no print/export, CI independent of credential). Vercel env var = **RB-3** (acceptor only). #35–#40 do NOT stop for the Vercel key; #41 AC-V2-17(c) and the observation part of AC-V2-22 are **BLOCKED** (not FAIL) until the acceptor enters `CWA_API_KEY` into Vercel.

## Orchestrator binding (Bindings §3.3, §3.4)

- Session `05b8408b-260a-46d3-a4fe-ec07e3ec365a` (main session, not a subagent).
- Mapping (Bindings §3.1, Model Profile default v2.2): `orchestrator` → `claude-opus-4-8` / `high`.
- **Verification (§3.4 last paragraph — main session via session transcript)**: transcript `~/.claude/projects/D--nchu-2026-AIoT-git-repository-aiot-classwork/05b8408b-….jsonl` — all assistant messages `claude-opus-4-8` / `high` (most recent and every prior). **PASS, no repair needed** (contrast V1 run which repaired xhigh→high).

## Model diversity note (Bindings §5)

Under the b2 `executor` override, `executor` = `claude-opus-5-5` and `primary_reviewer` = `claude-opus-5-5` are the **same model**. Per Bindings §5 this is legal (diversity is a preference, not §2.3 independence). Each Ticket/Spec audit record with Executor=opus-5-5 and Primary Reviewer=opus-5-5 MUST record `diversity_lost` in its independence note. Diversity is restored only if the Executor falls back to `claude-opus-4-8`.

## Preflight (2026-09-25; unattended-run policy §6 P-1…P-8)

| # | Check | Result |
| --- | --- | --- |
| 1 | Orchestrator binding `claude-opus-4-8` / `high` | **PASS** — verified via session transcript (no repair) |
| 2 | Branch / worktree state | `main` @ `08e158e`, clean (only untracked `grep.exe.stackdump` at repo root — junk, outside unit, not committed). Topic branch `home_work_01-v2-implementation` created @ `08e158e` = **BASE** |
| 3 | Accepted OC-V2 + effective SPEC-V2 v2.2 | **PASS** — read on disk; OC-V2 ACCEPTED §9 (acceptor verbatim §9.1); SPEC-V2 v2.2 DERIVED/effective §0 |
| 4 | Tickets #35–#41 + dependency graph | **PASS** — all OPEN, `ready-for-agent`; native `issue_dependencies_summary` matches declared graph (7 edges: 35→36, 36→37, 36→38, 38→39, 39→40, 37→41, 40→41; #35 blocked_by=0 = frontier) |
| 5 | `.env` exists (no secret printed) | **PASS** — `home_work_01/.env` exists, untracked (`git ls-files home_work_01/.env` empty) |
| 6 | GitHub access | **PASS** — `gh` authed `yotsubamomo`, admin/push/triage |
| 7 | `HW01_DEPLOY_URL` | **PASS** — repo variable = `https://aiot-hw01-weather.vercel.app` |
| 8 | Python 3.12 via uv | **PASS** — `.python-version=3.12`, uv 0.12.18; `.venv` present |
| — | Binding dry-run record (gov-* 6/6 + b2 executor override) | **PASS** on disk (`docs/governance/binding-verification.md`) |

## Activation preconditions (orch-default §3; OC-V2 §8)

| # | Precondition | Status |
| --- | --- | --- |
| 1 | Acceptor-accepted OC covering the run scope | **MET** — OC-V2 §9.1 verbatim acceptance 2026-09-25 |
| 2 | DA-derived, versioned, implementation-ready Spec/Tickets + derivation record | **MET** — SPEC-V2 v2.2; Tickets #35–#41; `derivation-SPEC-V2.md` §15 |
| 3 | §5.1 seven bindings ready & verifiable; six roles + subagent definitions exist; no `TBD` | **MET** — `.claude/agents/gov-*.md`; Bindings b3 §3.1 |
| 4 | §2.3 independent-dispatch mechanism declared in Bindings | **MET** — Bindings §3.4, §3.5 |
| 5 | Work-record authoritative locations configured (incl. derivation records) | **MET** — Bindings §7 |

All five hold → run activated.

## Work item status / frontier

| # | Status | Subject (BASE..HEAD) | Audit | Notes |
| --- | --- | --- | --- | --- |
| #35 | **audit 中 (R1 BLOCKING → correction → R2)** | `08e158e..c9c9ec5` (code anchor `bbc1d56`) | R1 BLOCKING (F-1) | V2 Core; server-side Latest Observation `/api/`, 4 failure classes, security re-scope; H-1/H-2/H-3 |
| #36 | 待執行 (blocked_by #35) | | | V2 Core; Now/Forecast mode |
| #37 | 待執行 (blocked_by #36) | | | V2 Core; Refresh & status semantics |
| #38 | 待執行 (blocked_by #36) | | | V2 Core; Taiwan→County→Station drill-down |
| #39 | 待執行 (blocked_by #38) | | | V2 Core; map fencing & responsive |
| #40 | 待執行 (blocked_by #39) | | | V2 Radar; radar overlay + 1 km alignment oracle |
| #41 | 待執行 (blocked_by #37,#40) | | | INTEGRATION/FINAL VERIFICATION; AC-V2-17(c) & AC-V2-22 obs part BLOCKED on Vercel key |

Frontier (READY, blocked_by=0): **#35**. Preferred schedule order (Bindings §6 parallelism-1 preference, not an edge): #35→#36→#37→#38→#39→#40→#41.

## Checkpoints / routing / replacement / rollover

- 2026-09-25 activation: re-grounded from disk (Bindings b3, OC-V2, SPEC-V2 v2.2, tickets-v2, orchestrator contract, gov-orchestrator def, V1 run record); all gates + preflight PASS; BASE `08e158e`; run record created (`305dd1c`); dispatching #35 Executor.
- 2026-09-26 #35 Executor return: **DONE**, subject `08e158e..c9c9ec5` (code anchor `bbc1d56`; worklog commits `9147997`,`c9c9ec5` under `doc/governance/`). **Binding (§3.4)**: agent `a1eef729c5e6bcebf` = `gov-executor`, observed `claude-opus-5-5`/`high` — matches mapping (b2 override). Machine-gate presence: commits on branch; worklog `worklog/issue-35.md` exists; `.env` untracked (`git ls-files` empty); all changed files inside `home_work_01/` (RB-5 held); no key literal in diff. New `observation.py` + `GET /api/observations/latest` in `server.py`; 385 tests (was 259/144-V1 preserved); CI run `36161275690` on branch. Sufficiency deferred to R1 (§3.8). Executor-flagged concerns (verbatim, unadjudicated, to be routed only if R1/verification surfaces them): (1) Vercel function time-limit assumption (10 s) — derivation §11 #1, instrument for #41 preview, DA if lower; (2) README deploy/Vercel-key section deferred to #41. Dispatching #35 R1 (fresh Primary Reviewer). **diversity_lost** applies (Executor opus-5-5 = Primary Reviewer opus-5-5).
- 2026-09-26 #35 R1 audit: record `audit/issue-35-c1-r1.md`, **VERDICT: BLOCKING (F-1)**. **Binding (§3.4)**: agent `ab39e3a58cdb76117` = `gov-primary-reviewer`, observed `claude-opus-5-5`/`xhigh` — matches; `diversity_lost` recorded. **F-1 (Medium, blocking, H-3)**: `990` treated as a universal missing-value sentinel across all numeric optional fields, nulling real `AirPressure "990.0"` (stations `C0F9I0`,`CAF030`) — but Spec data standard V1.05 / BRIEF-V2 §3.2 define `990` as the *variable-wind-direction* indicator only, not a pressure/rainfall missing code; breaks R-V2-OBS-3, R-V2-DD-7, H-3 "as published", AC-V2-03; tests `test_observation.py:217-219,:844` lock the wrong behavior in. Reviewer notes A-3 forbids FA-alone deferral (H-3 high-risk). Non-blocking: F-2 (Medium; lock held for whole upstream request → concurrent stall queues; owner #37 browser-30s + #41 Vercel timing/concurrency), F-3 (Low; non-string CountyName → whole-response fail; CWA always sends string), F-4 (Low; README:411-412 "deployed function needs no secret" → #41 R-V2-DOC-1(11)). Everything else in #35 scope PASS (AC-V2-04/05 all 8 counter-examples/06/07/16/17(a)(b)(d)(e)/20; 4 failure classes leak-clean at DEBUG with planted key; H-1/H-2/V1 regressions — teacher SQL 6/7, forecast byte-identical air-gapped, 385/385 tests, CI green; INV-V2-1/2/4/6/8; static re-scope add-only). **Routing**: F-1 is contract-internal (reviewer established the Spec semantics; no competing reading asserted) → Executor targeted correction; DA only if a per-field sentinel mapping proves genuinely ambiguous. Continuing Executor `a1eef729c5e6bcebf` (same worklog identity).

## Spec-level audit & phase acceptance

(pending — after all Tickets closed: Spec Integration Audit `audit/spec-SPEC-V2-c1-*.md`, then DA phase acceptance.)

## Terminus / completion report

(pending.)
