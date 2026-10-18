# HW2 — Re-Grill Brief Draft v0.1

- **狀態**：DISCUSSION DRAFT（2026-10-18）。這是 HW2 重新開始的 Grill 紀錄，不是 Outcome Contract，不是 Spec，不授權任何實作。
- **起點**：branch `home_work_02-regrill`（自 `main` 建立，commit `12fff506`），只含老師的需求來源。
- **舊紀錄**：先前的 Grill（G1–G8、C1–C5）、Outcome Contract r4、Spec v1.1，以及 OC v2 草稿與 F-1～F-7、U-1～U-5 的裁決，都保留在 branch `home_work_02-outcome-contract` 與 `home_work_02-rebaseline-oc-v2`，作為歷史參考。**本次 Grill 不沿用任何舊決定**，除非 acceptor 在本 Brief 中重新確認。
- **撰寫者**：無角色主 session（Bindings b5 §3.5）。Grill 不創造 authority（治理 §3.2）。
- **Governance**：`home_work_02/` governance on（Bindings b5）。本 Grill 收斂到新的 Outcome Contract 草稿。

**Statement classes**：
- **[T]** 老師的 HW2 作業頁文字（SRC-1／SRC-2）；
- **[X]** 老師提供的範例（SRC-3）；
- **[D]** acceptor 在本 Grill 的決定（逐字或忠實摘要，附日期）；
- **[F]** 查證過的事實；
- **[R]** 起草建議，經 acceptor 裁決才有效。

## 1. 來源登錄

| ID | 檔案（`doc/requirement/`） | 性質 | sha256 | 追蹤 |
| --- | --- | --- | --- | --- |
| SRC-1 | `HW2-requirements-Multiple Linear regression.txt` | acceptor 轉寫的 iLearning HW2 作業頁（2026-10-14 版） | `a969e7e2228e97a35027ad63d3747f2e502bdd685cf7cfca30aaab50048761ab`（git blob 內容） | 追蹤 |
| SRC-2 | `HW2-requirements-Multiple Linear regression.pdf` | iLearning HW2 作業頁列印（老師 2026-10-18 更新；列印 2026-10-18 02:59；4 頁）。正文與 SRC-1 相同，另有「==== 補充 ====」段 | `1b3a5aad1c261425eb34f2eb46aebe6a62c73aba4fbf2d67a166fe9df28639d7` | 不追蹤（單元 `.gitignore`；acceptor 2026-10-18 決定不公開） |
| SRC-2T | `HW2-requirements-Multiple Linear regression_SRC-2_2026-10-18.txt` | SRC-2 的忠實、標示頁碼的轉寫 | git blob `d185f89d5a3d923e24bb581eecd95481cfe2f335`；內容 sha256 `e5eb6a315dd5860e7562467012c748911454becb0c6bccde95823d1f0834e77c` | 追蹤 |
| **SRC-3** | `50 Startups_ Multiple Linear Regression & Feature Selection Explorer.pdf` | **需求範例**：老師在 week06 DIC-2 練習提供的成果網站列印檔（5 頁，1,203,722 bytes；PDF CreationDate `D:20261014105849+00'00'`＝2026-10-14 18:58 +0800）。<br>網站 `https://huanchen1107.github.io/AIoT-DIC2-MultipleLR/`；原始碼 `huanchen1107/AIoT-DIC2-MultipleLR`（public），commit `8b65e3bd9745e650ae7bea28f9562c059d5029ed`（2026-10-14 03:59 UTC；2026-10-18 查詢時仍是 HEAD，與 `week06/doc/spec/SPEC.md` 固定的 commit 相同） | `388a78c0af7dcf40996b9068f8d640cda654902023b671d205abdd67998f4789`（與 acceptor `~/Downloads` 的副本相同） | **追蹤**（acceptor 2026-10-18 決定 commit PDF） |

### 1.1 SRC-3 的證據性質

- [D] acceptor 2026-10-18：「這一份是需求的範例，來源是week06 的練習項目，最終交付是會需要這個網站一樣的發佈的。」
- [F] 範例網站的內容：
  - 50 Startups 資料集；
  - 比較 Lasso、Forward SFS、RFE、ElasticNet、Exhaustive Search 五種特徵選擇，k = 1～5；
  - 指標 Test RMSE、R²、Adjusted R²、MAE、F-statistic；
  - OLS 方程式與係數表（標準誤、t、p-value、95% 信賴區間、VIF）；
  - 即時預測器；
  - Test 殘差排行；
  - 頁尾的參考資料與致謝。
- [F] 範例 repo 沒有授權條款（GitHub `license: null`），所以只能參考它的形式與呈現，**不能複製程式碼、文案或資料**。它的部署設定包括 GitHub Pages workflow 與 Vercel（`api/`、`vercel.json`）。
- [R] **範例說明的是交付的形式，不是 HW2 的內容規格。** 範例中的具體項目——資料集、五種方法、k 的範圍、各項指標與圖表——不會自動成為 HW2 的要求；要逐項在 Grill 中決定。HW2 的作業文字（SRC-1／SRC-2）仍是內容要求的依據。
- [F] 範例網站的資料集（50 Startups，4 個特徵）本身不符合 HW2 的「10 至 20 個特徵」。這也說明它是形式範例，不是 HW2 的解答。

## 2. Frontier 紀錄

### Frontier 1 — 網站交付（進行中）

**證據**：
- [T] HW2 正文只寫「(optional) 若上傳至 GitHub，或是以colab撰寫，需提供連結，並在 README.md 中整理流程與成果。」沒有提到網站。
- [X] SRC-3 是發佈的成果網站。
- [F] 本 repo 的 `main` 已以 GitHub Pages 發佈 week06 的同類網站（`/week06/`）。

**acceptor 決定（2026-10-18）**：

| 項目 | 決定 | 說明 |
| --- | --- | --- |
| 1a. SRC-3 的登錄 | [D] 登錄為 SRC-3，PDF 一併 commit | 第 1 節 |
| 1b. 義務的來源 | [D] **老師有要求（有出處）** | 報告將標「老師要求」。**出處尚待 acceptor 提供**（日期、場合或檔案），用來記錄這個要求；在提供前，這一項是「老師要求、出處待補」 |
| 1c. 發佈形式 | [D] **靜態網站＋GitHub Pages** | 比照 week06：結果在分析程式中預先計算並匯出，網站以靜態檔案呈現與互動，發佈在本 repo 的 GitHub Pages。不需要伺服器、部署帳號或金鑰 |

**尚未決定**：
- 1b 的出處內容。
- 1d. 網站和 HW2 必交項目（主程式 `.py/.ipynb`、PDF 報告、學號 ZIP）的關係：是加在它們之外的交付，還是可以取代其中某一項。
- 1e. 網站的內容範圍。範例的哪些區塊是必要的，例如方法比較、k 的路徑、係數表、預測器、殘差。這屬於之後的 frontier，與分析方法的決定一起處理。

## 3. Revision history

| Version | Date | Change |
| --- | --- | --- |
| v0.1 | 2026-10-18 | 重新開始的 Grill：來源登錄 SRC-1～SRC-3；Frontier 1 的 1a～1c 決定 |
