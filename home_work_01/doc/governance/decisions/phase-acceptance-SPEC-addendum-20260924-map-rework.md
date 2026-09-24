# Phase-acceptance 增補紀錄 — Taiwan Map 視覺重做（#28）

- **性質**：DR-20 §3.5(B) 規定的 Orchestrator 自主增補。依治理 §3.8「審視變更是否影響 Reviewer／DA 判定的要件」判定，**不是**新的 phase acceptance，**不是** release authorization。
- **作者／時機**：Orchestrator（`gov-orchestrator`，`claude-opus-4-8`／`high`），#28 A-4 audit closure 之後。依 DR-20 §3.5(B)「這仍是 Orchestrator 依規則的自主判定，不需再問 DA」。
- **前置**：治理 §4.7 對 Lightweight 不再做 Spec Integration Audit；#28 subject 非 FA 授權的 rework cycle，故 closure 後才產出本增補。
- **日期**：2026-09-24。

## 1. Accepted phase subject 不變

原 phase acceptance（[`phase-acceptance-SPEC.md`](phase-acceptance-SPEC.md) §10）的 accepted subject 仍為 **`720c0a0`**。本增補不改變該裁定；#28 的 subject `5136bd2` 是疊加在其上、合併前的 post-baseline Lightweight 強化，經證實**未擾動** phase acceptance 的 coverage。

## 2. 依據的已 closure 紀錄

| 紀錄 | 狀態 | 用途 |
| --- | --- | --- |
| [`../audit/spec-SPEC-c1-r1.md`](../audit/spec-SPEC-c1-r1.md) | CLOSURE（`720c0a0`） | Spec 級整合結論；在 `720c0a0` 之上仍有效，#28 diff 觸及的部分（地圖卡、靜態檢查、README、ACCEPTANCE）由 #28 獨立審查另行證明 |
| [`../audit/issue-28-c1-r1.md`](../audit/issue-28-c1-r1.md) | R1 = BLOCKING（F-1/F-2/F-4/F-5） | A-4 independent audit 第一輪（`gov-primary-reviewer`） |
| [`../audit/issue-28-c1-r2.md`](../audit/issue-28-c1-r2.md) | R2 = BLOCKING（N-1，evidence defect） | closure review；F-1..F-5 確認修復 |
| [`../audit/issue-28-c1-alt.md`](../audit/issue-28-c1-alt.md) | **AUDIT CLOSURE** | §4.4 唯一一次 Alternate Independent Review（`gov-alternate-reviewer`，fresh context） |
| [`decision-20260924-taiwan-map-rework.md`](decision-20260924-taiwan-map-rework.md)（DR-20） | EFFECTIVE | lane／boundary／§3.6-A HOW 採納／核定文逐字 |
| [`decision-20260924-map-rework-rs1-rs2.md`](decision-20260924-map-rework-rs1-rs2.md)（DR-21） | EFFECTIVE | RS-1（V-2 以 2px 白描邊界定 PASS）、RS-2（masthead 一句 in-boundary incidental change） |

## 3. Binding 核對（§3.4，全部通過）

| 角色 | agentType | model／effort | 對照 model-profile-default-v2.2 | agentId |
| --- | --- | --- | --- | --- |
| Executor | `gov-executor` | `claude-opus-4-8`／`high` | ✅ `executor` | `a37f68bb30f67b595` |
| Primary Reviewer（R1＋R2） | `gov-primary-reviewer` | `claude-opus-5-5`／`xhigh` | ✅ `primary_reviewer` | `abca3f739e1523101` |
| Alternate Reviewer | `gov-alternate-reviewer` | `claude-fable-5-1`／`xhigh` | ✅ `alternate_reviewer` | `a54c21ed421c6f833` |
| Orchestrator | `gov-orchestrator` | `claude-opus-4-8`／`high` | ✅ `orchestrator` | 主 session |

## 4. Diff-scope rollup（`720c0a0`..`5136bd2`，§3.5(B)(A)）

**實作／測試檔（doc 之外）僅 7 個，全部在 Taiwan Map 卡邊界內**：

- `home_work_01/static/index.html`（地圖卡標記結構、面板/圖例；masthead 一句 in-boundary，DR-21.2）
- `home_work_01/static/app.js`（地圖初始化、藥丸、面板、resize 只在寬度/版面模式改變時 re-fit）
- `home_work_01/static/styles.css`（地圖卡樣式、藥丸、面板/圖例）
- `home_work_01/static/data/basemap.js`（vendored 向量底圖；執行期零外部請求）
- `home_work_01/tests/test_map_frontend.py`、`home_work_01/tests/test_static_checks.py`（新增/強化測試）
- `home_work_01/README.md`（Taiwan Map 段：底圖來源/授權、免金鑰、代表點為專案定義、Select Date 位置）

**未觸及**（INV-2／INV-9 完好）：`app.py`、`server.py`、`weather_query.py`、`api/`、`vercel.json`、`data.db`。Grading App／MVM／`/api/` 形狀不變。

## 5. Phase 影響判定（§3.8）

- **契約不變量全部維持**：H-2（概念詞逐字，`index.html` 概念詞未變）、H-3（藥丸值/色直接取 `/api/days/<date>`，七日 126/126 parity，前端零重算）、R-EN-4/5/6/7、R-SHR-4、R-SEC-1..3、INV-2/7/9。
- **AC 重驗**：AC-17／AC-18／AC-19 於 #28 audit 逐項 PASS（截圖證據齊備，含修正後的真 loading state）；AC-04 走 §2.2 vendored 向量底圖，不改靜態檢查白名單、執行期零外部請求。
- **回歸**：offline 套件 `164 passed`；CI 綠（subject `5136bd2` 與 HEAD `5d8b169`）；金鑰掃描 0 筆（536 tracked）。
- **Preview smoke（Orchestrator，2026-09-24，branch alias）**：`/`=200、`/api/health`=200（6 區／7 日）、`/api/days`=200、`/api/days/2026-09-24`=200（六區 `derivedMapTemperature`+`colourBand`）、`/api/regions`=200、六區 `/api/regions/<region>/series` 全 200（編碼中文路徑，#21 修復完好）。URL：`https://aiot-hw01-weather-git-homework01-hw10-im-8efc12-nchu-aiot-class.vercel.app`。

**結論**：#28 的變更不影響 `phase-acceptance-SPEC.md` §10 對 `720c0a0` 的 phase acceptance 要件；`spec-SPEC-c1-r1.md` 的 Spec 級結論在 `720c0a0` 之上仍成立，#28 觸及面由其獨立審查（R1→R2→Alternate CLOSURE）另行證明。合併時，release 候選 subject 為 `5136bd2`，與 `phase-acceptance-SPEC.md` 的 `720c0a0` 一併適用。

## 6. 保留（未由本 run 執行）

- **RB-1**：合併進 `main` 保留給 acceptor。**RB-2**：繳交保留給 acceptor。本 run 不合併、不提交。
- 既有 acceptor／post-merge 項目（AC-22(c) 合併後 `workflow_dispatch`、AC-15 production smoke、Vercel dashboard build-log/Root-Directory/無金鑰確認）維持原記載，不受本增補影響。
- 另立票：#18 R2 N-1（`--acquired-at` 格式驗證）為獨立 Lightweight work item，自帶 A-4 audit，不與 #28 混同。
