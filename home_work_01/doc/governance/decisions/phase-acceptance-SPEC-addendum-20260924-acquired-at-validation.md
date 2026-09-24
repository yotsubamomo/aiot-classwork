# Phase-acceptance 增補紀錄 — Ingestion 取得時間格式驗證（#29）

- **性質**：DR-22 §5(B) 規定的 Orchestrator 自主增補（同 DR-20 §3.5(B) 兩段式）。依治理 §3.8「審視變更是否影響 Reviewer／DA 判定的要件」判定，**不是**新的 phase acceptance，**不是** release authorization。
- **作者／時機**：Orchestrator（`gov-orchestrator`，`claude-opus-4-8`／`high`），#29 A-4 audit closure（R2）之後。
- **日期**：2026-09-24。

## 1. Accepted phase subject 不變

原 phase acceptance（[`phase-acceptance-SPEC.md`](phase-acceptance-SPEC.md) §10）的 accepted subject 仍為 **`720c0a0`**。#28 之後 accepted 疊加集合再加上 #29 的 subject `ee84480`；#29 經證實**未擾動** phase acceptance 的 coverage，也未改變任何已提交交付物的位元內容。

## 2. 依據的已 closure 紀錄

| 紀錄 | 狀態 | 用途 |
| --- | --- | --- |
| [`decision-20260924-acquired-at-validation.md`](decision-20260924-acquired-at-validation.md)（DR-22） | EFFECTIVE | lane（Lightweight）、boundary allowlist、驗證接受準則（依 DR-17）、H-3/H-1、兩段式整合證據要求 |
| [`../audit/issue-29-c1-r1.md`](../audit/issue-29-c1-r1.md) | R1 = BLOCKING(F-1) | A-4 independent audit 第一輪（fresh `gov-primary-reviewer`）；F-1 = validator `\d` 收非 ASCII 數字，違反 AT-2 |
| [`../audit/issue-29-c1-r2.md`](../audit/issue-29-c1-r2.md) | **R2 = AUDIT CLOSURE** | F-1／F-2／F-3 修復確認、零回歸、blobs 不變、259 綠；F-4/F-5 disposition adequate |
| [`../audit/issue-18-c1-r2.md`](../audit/issue-18-c1-r2.md) §5 N-1 | 來源 finding | 本 work item 修正的原始 Medium finding |
| DR-17（`decision-20260924-ingestion-timestamp-semantics.md`） | EFFECTIVE | 取得時間＝「最後更新時間」語義；驗證準則的 grounding |

## 3. Binding 核對（§3.4，全部對照 model-profile-default-v2.2 通過）

| 角色 | agentType | model／effort | agentId |
| --- | --- | --- | --- |
| Design Authority（DR-22） | `gov-design-authority` | `claude-fable-5-1`／`xhigh` | `a50b4ef41f367d729` |
| Executor（含 R1 correction） | `gov-executor` | `claude-opus-4-8`／`high` | `a068f9df30c34349e` |
| Primary Reviewer（R1＋R2） | `gov-primary-reviewer` | `claude-opus-5-5`／`xhigh` | `afd86af32279b362c` |
| Orchestrator | `gov-orchestrator` | `claude-opus-4-8`／`high` | 主 session |

## 4. Diff-scope rollup（`cc29c7f`..`ee84480`，DR-22.5(A)）

實作／測試（doc 之外）：

- `home_work_01/ingestion/acquisition_time.py`（新 validator：`re.compile(..., re.ASCII)` + `fullmatch`；曆法有效性）
- `home_work_01/ingestion/pipeline.py`（三套用點之 CLI 與 online 驗證；`main` fail-closed 連線）
- `home_work_01/ingestion/provenance.py`（sidecar `acquiredAt` 驗證，移除 `str()` 轉型）
- `home_work_01/tests/test_acquisition_time.py`（+95 測試，259 全綠）
- `home_work_01/README.md`（ingestion「取得時間格式」段：ASCII 數字、fail-closed、不 fallback）
- `home_work_01/doc/acceptance/ACCEPTANCE.md`（§6 N-1 列 → FIXED in #29）

**未觸及**（byte-identical to `cc29c7f`）：`data.db`、raw JSON、sidecar 內容；`derive.py`／`config.py`／`persist.py`／`fetch.py`／`/api`／`static`／`vercel.json`／`server.py`／`app.py`／`weather_query.py`。

## 5. Phase 影響判定（§3.8）

- **契約不變量維持**：DR-17 取得時間語義不變（T-1..T-4 綠）；R-DB-5（`+08:00`）；INV-2/3/5；H-3（「最後更新時間」值只做格式把關、不讀時鐘、不正規化）、H-1（失敗訊息含值/來源/格式、無金鑰，哨兵掃描零外洩）。
- **AC-12**：clean-export（無 `.env`、封網）重建 `data.db` 與提交值逐位元相同，`ingestedAt = 2026-09-24T02:24:50+08:00`（提交 sidecar 值在新規則下合格）。
- **回歸**：offline 套件 `259 passed`（parent 164 → #29 259，既有全數保留未弱化）；CI 綠（`ee84480`，push run `35982002167`／PR run `35982005624`）；金鑰掃描 0。
- **部署面**：無變更（`/api`、`static`、`data.db` 未動）→ 不需另做 preview smoke；#28 closure 時的 preview smoke 仍代表現行部署面。

**結論**：#29 為純 ingestion 端的 fail-closed 格式把關，強化 DR-17 取得時間標示的誠實性，未改變任何已接受交付物、Spec、Outcome Contract 或部署行為。release 候選集合＝`phase-acceptance-SPEC.md` 的 `720c0a0` + #28 `5136bd2` + #29 `ee84480`，合併時一併適用。

## 6. 保留與備註

- **RB-1**：合併進 `main` 保留給 acceptor。**RB-2**：繳交保留給 acceptor。本 run 不合併、不提交。
- **F-4（attribution）**：commits `cc29c7f`、`bd52ede`、`b4b121f` 帶 `Co-Authored-By: Claude` trailer（Orchestrator 誤依 session reminder，違反 CLAUDE.md:98）。acceptor 2026-09-24 裁定 **leave for squash-merge**；不改已 push 歷史（RB-6 保留）。**合併備註**：GitHub 預設 squash message 會帶入被 squash commit 的 co-author 行——acceptor 於合併時需編輯 squash message，避免該 trailer 進入 `main`。R1 correction 之後所有 commit（`ee84480`、`def4597` 及本 closure commit）皆無 attribution。
- **R2-O1（Low，不延長 cycle）**：若 validator 呼叫點改回 `.match`，259 測試仍全過（`strptime` 會擋多餘字元）——僅為測試強度弱點，行為仍正確。owner Executor，可選。
