# HW2 — House Price Prediction | Grill Brief Draft v0.3

**Status:** DISCUSSION DRAFT — the Grill closure input for the Outcome Contract. Not accepted, not an authoritative Spec, no implementation authorization.
**Date:** 2026-10-14
**Supersedes:** v0.2 (kept unchanged as history; change log in §11).
**Source of authority:** the teacher's `HW2-requirements-Multiple Linear regression.txt` for coursework obligations; G1–G8 plus clarifications C1–C4 for project choices. `week05/multiple_linear_regression_crisp_dm.ipynb` is a reference implementation only.
**Governance:** `home_work_02/` is governance **on** (Project Bindings b4). This Grill closes into the Outcome Contract draft `home_work_02/doc/governance/outcome-contract.md`. Only that contract, with the acceptor's acceptance record, becomes authoritative. The Spec is derived afterwards by the Design Authority.

**Statement classes:** **[T]** teacher requirement · **[G]** confirmed Grill decision G1–G8 (original wording) · **[C]** clarification decision recorded 2026-10-14 (C1–C4) · **[R]** recommendation; binding only if carried into the accepted Outcome Contract · **[F]** verified fact (evidence in §10).

## 1. Outcome
Build a reproducible CRISP-DM analysis that predicts King County house sale prices with linear-regression models. Compare a multiple-LR baseline, forward- and backward-selected LR, Ridge and Lasso under group-aware nested cross-validation on the Fit partition. Freeze the selected predictor, attach 95% split-conformal prediction intervals calibrated on a separate partition, and evaluate it once on an untouched Test partition. Deliver the notebook, the supporting modules and tests, the report PDF, the authentic AI-conversation PDF and the ID-named ZIP.

## 2. Teacher-required outcomes (unaltered in meaning) [T]
- Kaggle public dataset with 10–20 features; name and source URL.
- Use linear regression for predictions; simple, multiple, or auto-regression may be attempted.
- Feature Selection and Model Evaluation must be performed.
- Prediction plot with a confidence interval **or** prediction interval.
- CRISP-DM: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment.
- Export all ChatGPT conversations as PDF with pdfCrowd or other means.
- Research web solutions to the same topic with NotebookLM, and put a summary of `100 字以上` in the report, labeled `NotebookLM 摘要`. **[R]** Read as at least 100 Chinese characters.
- Explicitly label `GPT 輔助內容`; compare and explain mainstream or better internet solutions.
- Submit `7114056XXX_hw2.py/.ipynb` and the PDF report, together with supporting files and directories, as `7114056XXX_hw2.zip` (placeholder replaced with the actual student ID).
- If GitHub is used or the work is written in Colab, provide the link and a README.md describing the workflow and results.
- Deadline shown: 2026-11-04. Assessment: documentation 50%, results 50%. The "Kaggle 名次 (若有)" item does not apply: this dataset has no competition leaderboard. **[F]**

## 3. Confirmed Grill decisions [G] — original wording, not edited
| Decision | Confirmed choice |
|---|---|
| G1 | House price prediction; Kaggle **King County House Sales**; target `price`; comparison scope: multiple LR baseline + forward/backward feature selection + Ridge/Lasso |
| G2 | Initial 80/20 Development/Test partition, model and feature selection with 5-fold CV within training data; rank candidates primarily by CV RMSE; also report R²/MAE/MSE |
| G3 | 95% **Split Conformal Prediction** intervals; independently compute observed coverage and average width |
| G4 | Partition entire data into 60% Fit / 20% Calibration / 20% Test; only Fit may guide model selection; Calibration only calibrates frozen predictor; Test only for final evaluation |
| G5 | Modular Python + Notebook; notebook is principal classroom-facing program, modules for data, selection, modeling, evaluation and conformal; week05 notebook is only a reference |
| G6 | Main analysis report PDF with NotebookLM summary and AI-assistance labels, plus separate **authentic** ChatGPT conversation export PDF |
| G7 | Existing `https://github.com/yotsubamomo/aiot-classwork` repository, HW2 subfolder, local Python/Jupyter; zip is formal school submission |
| G8 | Standard verification: module tests, leakage tests, conformal calculation verification, full notebook rerun, and submission document checks; Git push and iLearning submission reserved for human operation |

## 4. Clarification decisions [C] (acceptor, 2026-10-14)
These clarify G1–G8. They do not replace the original wording; where wording differs, the clarification states how the original is read.

| ID | Clarifies | Decision |
|---|---|---|
| C1 (Q1) | G2, G4 | The G2 "Development" set (80%) = 60% Fit + 20% Calibration. "Training data" in G2 means **Fit**. All model selection and all cross-validation happen within Fit. |
| C2 (Q2) | G2, G4 | Splitting into Fit / Calibration / Test and every CV fold are **group-aware on house `id`**: all sales of one house stay in one partition and one fold. |
| C3 (Q3) | G2 | All candidates are compared on **identical outer 5-fold** splits of Fit. Feature count (forward/backward) and hyperparameters (Ridge/Lasso `alpha`) are chosen by **inner CV inside each outer training fold**. G2 "5-fold CV" is the outer comparison; G2 stays the original decision. |
| C4 (Q4) | G3, G2 | Models are trained on **log(price)**. Conformal scores are calibrated on the log scale and intervals are back-transformed to USD. Comparison and evaluation metrics (RMSE, MAE, MSE, R²) are reported in **original USD**. |
| — (Q5) | — | The student ID will be supplied by the acceptor before final packaging. |

## 5. Method boundaries
### 5.1 Data [F] / [R]
- **Pinned source:** Kaggle `harlfoxem/housesalesprediction`, CC0-1.0, `kc_house_data.csv`, checksums in §10. A different archive is a re-pin and must be recorded.
- **Feature-count rule:** count **source features** (raw CSV columns other than the identifier `id` and the target `price`). Encoded columns are not counted. Result: 19 with `date`, 18 without; the requirement holds under either treatment.
- **`id`:** identifier and grouping key only (C2); 177 repeat-sale rows, 21,436 houses.
- **`date`:** dropped or turned into a derived sale-time feature; the choice is documented (Spec).
- **`zipcode`:** nominal; never used as a raw magnitude (encoding is a Spec decision).
- **Exact dependency:** `sqft_living = sqft_above + sqft_basement` in every row. The LR design matrix must have full column rank, with the resolution documented (Spec).
- **Outliers and recoding** (e.g. `bedrooms` = 33, `yr_renovated` = 0 meaning "never"): decided from Fit only, documented.

### 5.2 Partition and isolation [G4, C1, C2]
- 60 / 20 / 20 group-aware random partition with a fixed seed. Sizes are approximate because whole houses are assigned.
- Test is evaluated once, after the predictor is frozen. Calibration is used only to compute the conformal quantile of the frozen predictor.
- Every fitted step (imputation, encoding, scaling, selection, hyperparameter search) is fitted on training-fold rows only.

### 5.3 Model comparison [G1, G2, C3, C4]
- Each candidate is a **candidate procedure** (preprocessing + selection + fit) evaluated on the same outer group-aware 5-fold split of Fit, scored by mean outer-fold RMSE in USD. R², MAE and MSE are also reported.
- Selection criterion inside procedures: CV error, not p-values.
- **Bias statement [R]:** each candidate's outer-CV score estimates the performance of that procedure. **Choosing the minimum among several candidates makes the winner's outer-CV score optimistically biased** (selection among noisy estimates). The independent estimate of the frozen predictor's performance is the single Test evaluation. Reports must not present the winner's outer-CV score as an unbiased estimate.
- The winning procedure is re-run on all of Fit to produce the frozen predictor. It is a refit, not the same object that produced the outer-CV scores; the report says so.
- **[R]** Back-transformation to USD (`exp` of a log-scale prediction) estimates the conditional median rather than the mean. Any bias correction is a Spec decision applied identically to all candidates.

### 5.4 Conformal prediction intervals [G3, C4]
- **Target:** the frozen predictor only. Intervals for other candidates are optional.
- **Method:** split conformal, score s = |log y − log ŷ| on Calibration (n_cal rows). q̂ = the ⌈(n_cal + 1)(1 − α)⌉-th smallest score, α = 0.05. Interval = [ŷ·e^(−q̂), ŷ·e^(q̂)] in USD; positive by construction.
- **Coverage claim and assumptions** (stated in the report; no stronger claim):
  - The guarantee is **marginal**: P(Y ∈ C(X)) ≥ 1 − α, averaged over the random partition and the test draw. It is not conditional on any feature value, price range or region.
  - It requires Calibration and Test units to be **exchangeable**. Group-aware splitting (C2) prevents the same house from appearing in two partitions, but **does not by itself establish exchangeability**. Here exchangeability comes from the **random assignment of whole houses** to partitions within this fixed dataset. The exchangeable unit is the house; within-house dependence affects the 177 repeat-sale rows. The per-sale statement is therefore approximate for that subset.
  - The guarantee covers held-out sales **from this dataset (May 2014 – May 2015)**. It does not transfer to later sales, other regions or a changed market: that is a deployment limitation, stated in the Deployment section.
  - Back-transforming by the monotone `exp` keeps coverage of the price interval equal to that of the log interval.
  - With continuous scores and no ties, coverage is also ≤ 1 − α + 1/(n_cal + 1).
- **Observed coverage** on Test is a single-split estimate with sampling error (about ±0.7 percentage points at n ≈ 4,300). Observed coverage ≠ 95% is not by itself a failure. It is reported together with the mean width, in USD.

## 6. Non-goals
No Web App, FastAPI, database, full MLOps, forced Kaggle ranking, or mandatory deep-learning or nonlinear models. No fabricated NotebookLM or GPT evidence. Reference-implementation behavior is not a teacher requirement. CRISP-DM *Deployment* = a saved frozen predictor plus a documented prediction function returning point and interval predictions, with usage limits (§5.4).

## 7. Evidence that only the acceptor can produce
| Item | Why only the acceptor | Teacher basis |
|---|---|---|
| ChatGPT conversation export PDF (pdfCrowd or equivalent) | Must be the acceptor's own, authentic conversations; Agents cannot have or create them | §4 AI協助要求; grading 15% |
| NotebookLM research and the ≥100 字 summary source | NotebookLM research is done by the acceptor; Agents may format but not invent the summary | §4 AI協助要求; grading 15% |
| Student ID | Personal identifier, not in the repository | §5 繳交內容 |
| Git push / GitHub link going live, iLearning ZIP upload | Reserved (G8; Bindings RB-1, RB-2) | §5 (optional GitHub) |

**[R]** Implementation is done with Claude Code, so the `GPT 輔助內容` section names the tools actually used, while keeping the teacher's label.

## 8. Remaining ambiguity check
No remaining ambiguity prevents an observable Outcome Contract. Open items are Spec-level design choices (column resolution for the exact dependency, `date` and `zipcode` treatment, bias correction, tie-break, report production method) or acceptor-provided inputs (§7). Items to confirm at acceptance:
- **G8 vs Bindings SA-1/SA-2:** G8 reserves Git push for the acceptor, which is narrower than the standing authorization for topic-branch push and PRs. The Outcome Contract follows G8 (Agents commit locally only) unless the acceptor states otherwise at acceptance.
- **File location:** the teacher file and briefs sit in `home_work_02/docs/`. Bindings §2.2 names `doc/requirement/` as the location of the upper contract. Recommended: move the teacher file there unchanged, and the briefs to `doc/brief/`, before acceptance.

## 9. Status and next step
Ready for the Outcome Contract draft (`home_work_02/doc/governance/outcome-contract.md`, draft r1). After the acceptance record: Design Authority confirms lane, high-risk categories and derives the Spec.

## 10. Dataset verification evidence [F]
Retrieved 2026-10-14 anonymously from the Kaggle public API (`api/v1/datasets/view|list|download/harlfoxem/housesalesprediction`) and inspected locally with pandas (session `8943ecf6`, scratchpad; data not added to the repository).

| Item | Value |
|---|---|
| Source | https://www.kaggle.com/datasets/harlfoxem/housesalesprediction — "House Sales in King County, USA", owner `harlfoxem`, datasetId 128 |
| License | CC0-1.0 (API `licenses[0].name`) |
| File | `kc_house_data.csv`, 2,515,206 bytes, Kaggle `creationDate` 2017-04-15T05:48:17Z |
| Archive sha256 | `1fdffaeec5e7656f6c09e29d9daa7e2157479c5f8e3a761758b4bfa43c773202` (798,275 bytes, as served 2026-10-14) |
| CSV sha256 | `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e` |
| Shape | 21,613 rows × 21 columns; 0 missing values; 0 duplicate rows; 21,436 unique `id` (177 repeat-sale rows) |
| Header | `id,date,price,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,grade,sqft_above,sqft_basement,yr_built,yr_renovated,zipcode,lat,long,sqft_living15,sqft_lot15` |
| Count rule → result | Source features = columns minus `id` and `price` → 19 (18 if `date` is dropped). Inside 10–20 either way |
| Notable | `sqft_living = sqft_above + sqft_basement` in all rows; `price` 75,000–7,700,000 USD (median 450,000); `zipcode` 70 values; `date` 2014-05-02 → 2015-05-27 (string `YYYYMMDDT000000`); `bedrooms` 0–33; `yr_renovated` = 0 in 95.8% of rows |

The archive sha256 depends on how Kaggle packages the download. The **CSV sha256 is the pin**.

## 11. Revision history
| Version | Date | Change |
|---|---|---|
| v0.1 | 2026-10-14 | G1–G8 dialogue captured; dataset hard check, conformal scope, reporting handoff and student ID left open |
| v0.2 | 2026-10-14 | Dataset verified (§10); G2/G4 reading note; data facts, comparison protocol and conformal scope proposed; questions Q1–Q5 |
| v0.3 | 2026-10-14 | Q1–Q4 recorded as clarification decisions C1–C4 (G1–G8 wording untouched); Q5 deferred to packaging; winner's-curse statement for outer CV vs Test (§5.3); exchangeability and coverage assumptions restated (§5.4); evidence only the acceptor can produce (§7); remaining-ambiguity check (§8); G8-vs-SA-1 and file-location items for acceptance |
