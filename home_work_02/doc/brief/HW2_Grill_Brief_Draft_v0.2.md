# HW2 — House Price Prediction | Grill Brief Draft v0.2

**Status:** DISCUSSION DRAFT — not accepted, not an authoritative Spec, no implementation authorization. v0.2 is a gap-closure revision of v0.1; it does not reopen G1–G8.
**Date:** 2026-10-14
**Source of authority:** Teacher's `HW2-requirements-Multiple Linear regression.txt` for coursework obligations; G1–G8 for confirmed project choices. `week05/multiple_linear_regression_crisp_dm.ipynb` is reference implementation only.
**Governance:** `home_work_02/` is governance **on** (Project Bindings b4). The Grill closes into an **Outcome Contract** (`home_work_02/doc/governance/outcome-contract.md`, Bindings §2.3) with an acceptor acceptance record. The Brief itself is never "accepted". The Spec is derived afterwards by the Design Authority.

**Statement classes used below:** **[T]** teacher requirement · **[G]** confirmed Grill decision (G1–G8) · **[R]** recommendation, derived from the inputs; it is binding only after acceptor sign-off · **[Q]** open question for the acceptor · **[F]** verified fact (evidence in §10).

## 1. Outcome
Build a reproducible CRISP-DM analysis that predicts house prices from a Kaggle public dataset with 10–20 features. Compare multiple linear regression against selected alternatives under controlled feature selection and independent evaluation, and produce a prediction plot with uncertainty intervals. Deliver code, evidence, the required PDF documentation and the ZIP.

## 2. Teacher-required outcomes (unaltered in meaning) [T]
- Kaggle public dataset with 10–20 features; name and source URL.
- Use linear regression for predictions; simple, multiple, or auto-regression may be attempted.
- Feature Selection and Model Evaluation must be performed.
- Prediction plot with a confidence interval **or** prediction interval.
- CRISP-DM: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment.
- Export all ChatGPT conversations as PDF with pdfCrowd or other means.
- Research web solutions to the same topic using NotebookLM, and put a summary of `100 字以上` in the report, explicitly labeled `NotebookLM 摘要`. 〔v0.2〕 Recommended reading: at least 100 Chinese characters. **[R]**
- Explicitly label `GPT 輔助內容`; compare and explain mainstream or better internet solutions.
- Submit `7114056XXX_hw2.py/.ipynb`, the PDF report, and supporting files and directories, packaged as `7114056XXX_hw2.zip` (the placeholder is replaced with the actual student ID).
- If GitHub is used or the work is written in Colab, provide the link and a README describing the workflow and results.
- Deadline shown: 2026-11-04. Assessment: documentation 50%, results 50%. The "Kaggle 名次 (若有)" item does not apply: this dataset has no competition leaderboard. **[F]**

## 3. Confirmed Grill decisions (project additions) [G]
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

〔v0.2〕 **Reading note on G2 and G4 (Q1).** The G2 text ("80/20", "within training data") and G4 ("60/20/20", "only Fit may guide model selection") describe the same partition only if the G2 Development set (80%) = Fit (60%) + Calibration (20%), and "training data" in G2 means **Fit**. v0.2 proposes this reading. Under the alternative reading, CV over the whole 80% would use Calibration for model selection and violate G4.

## 4. Intended workflow and boundaries
1. **Data.** Retrieve and pin the exact Kaggle archive; record source, license, row count, raw column list, feature roles and target. 〔v0.2〕 Done for the current archive: §10 shows the dataset satisfies the 10–20 requirement under every defensible count. The count is on **source features** (raw columns other than the identifier and the target), never on encoded columns. **[F]** Document the treatment of `id`, `date` and `zipcode` (§4.1).
2. **Split.** Deterministically split into 60/20/20 disjoint Fit, Calibration and Test partitions. Keep Test inaccessible until model selection is frozen. Train leakage-sensitive transformations and feature selection only inside each applicable CV training fold within Fit. 〔v0.2〕 Repeat sales of the same house are kept in one partition and one fold (Q2).
3. **Compare.** Evaluate the all-features linear regression, forward- and backward-selected LR, Ridge and Lasso with comparable Fit-only 5-fold CV. Select by CV RMSE with a documented tie-break and secondary evaluation. Learn hyperparameters only through the permitted Fit CV. 〔v0.2〕 Comparison protocol in §4.2 (Q3).
4. **Calibrate and test.** Freeze the chosen predictor and refit it on Fit only. Calibrate conformity scores on Calibration with the finite-sample conformal quantile (95% target), with no tuning on Calibration. Report test R², MAE, MSE, RMSE, marginal empirical coverage and mean interval width. Show actual vs predicted with bounds, plus other informative plots. 〔v0.2〕 Scale of scores and metrics in §4.3 (Q4).
5. **Document.** Produce a notebook and report covering all six CRISP-DM stages, reproducibility, limitations, literature comparison, source links, the verified NotebookLM study and the real GPT conversation export.
6. **Package.** Put the code, the needed supporting data and metadata (CC0-1.0, §10), reports, requirements and README into the school-submission ZIP. Do not push or submit without separate human action.

### 4.1 〔v0.2〕 Data facts that constrain preparation [F] / [R]
- **`id`** is an identifier, not a feature. 177 rows repeat an `id` (21,613 rows, 21,436 houses), i.e. repeat sales of the same house. It is kept only as a grouping key (Q2).
- **`date`** spans 2014-05-02 to 2015-05-27, as a string (`20141013T000000`). **[R]** Either drop it or derive a sale-time feature; whichever is chosen is documented in Data Preparation. The choice does not affect the 10–20 count (18 or 19 source features).
- **`zipcode`** (70 values) is nominal, not a magnitude. **[R]** Do not use it as a raw number. Encoding it is a modeling choice for the Spec. Encoded columns do not count toward the 10–20 rule (§4 step 1).
- **Exact linear dependency:** `sqft_living = sqft_above + sqft_basement` holds in every row. **[R]** Including all three makes the OLS design matrix rank-deficient: coefficients are not identifiable, and p-value-based backward elimination fails. Data Preparation must resolve this dependency and document it. Which column is dropped is a Spec decision.
- **Data quality:** no missing values and no duplicate rows. Outliers exist (`bedrooms` = 33; 13 rows with `bedrooms` = 0; 10 rows with `bathrooms` = 0). `yr_renovated` = 0 means "never renovated" in 95.8% of rows. **[R]** Any row filtering or recoding is decided from Fit data only and documented.

### 4.2 〔v0.2〕 Model-comparison protocol (fairness and selection bias) [R] / Q3
- Every candidate (all-features LR, forward LR, backward LR, Ridge, Lasso) is a **candidate procedure**: preprocessing + selection + fit, built as one pipeline.
- Candidates are compared on **the same outer 5-fold split of Fit** (same seed, same folds, group-aware per Q2). The score is the mean outer-fold RMSE on the **price scale** (per Q4).
- Internal choices (number of features for forward or backward selection, `alpha` for Ridge or Lasso) are made by an **inner CV inside each outer training fold**. Selecting features on all of Fit and then cross-validating the chosen subset is optimistic and not allowed.
- Scaling and encoding are fitted inside each training fold. Ridge and Lasso get standardized inputs; all candidates start from the same source-feature set.
- Selection uses a CV error criterion, not p-values. The week05 p-value elimination is reference only.
- After selection, the winning procedure is re-run on all of Fit to produce the frozen predictor. Test is never printed or consulted during selection. Unlike week05, the forward-selection loop must not report Test RMSE.

### 4.3 〔v0.2〕 Conformal interval scope [R] / Q4
- **Target:** the final selected model only. It is the one prediction plot the teacher requires. Intervals for other candidates are optional and not part of acceptance.
- **Score and quantile:** split conformal with score |y − ŷ| on the chosen scale. With n = |Calibration| and α = 0.05, the quantile is the ⌈(n+1)(1−α)⌉-th smallest score. The guarantee is **marginal** coverage ≥ 95% under exchangeability. No conditional coverage is claimed.
- **Scale (Q4):** prices are heavily right-skewed (US$75k–7.7M, median US$450k). On the raw scale, constant-width intervals can have negative lower bounds for cheap houses. Fitting on log(price) and conformalizing on the log scale gives positive, multiplicative intervals in price units. Because exp() is monotone, the marginal guarantee is preserved after back-transformation.
- **Evidence:** a test that recomputes the quantile index and empirical coverage independently of the production code (G8). Coverage below 95% on Test is reported, not hidden; it is not alone a failure.

## 5. Acceptance intent (draft; not authoritative ACs)
| Proposed AC | Observable evidence |
|---|---|
| A1 Dataset conforms | Original-source link, pinned archive/CSV checksum (§10), inspected raw header, and source-feature count stated with its counting rule |
| A2 Analysis complete | Notebook and report cover six CRISP-DM stages and execute |
| A3 Isolation | Disjoint split assertions; 〔v0.2〕 no `id` in more than one partition or fold; fitted preprocessing and feature selection stay within Fit CV training folds; Calibration and Test stay out of model tuning |
| A4 Core experiments | Repeatable comparison of baseline, forward/backward, Ridge and Lasso on identical outer folds; 〔v0.2〕 outer-CV RMSE on the price scale per candidate, then final holdout metrics for the selected model |
| A5 Conformal interval | Tested finite-sample quantile logic; plot of values with lower/upper bounds; Test empirical coverage and mean width; 〔v0.2〕 scale and score documented |
| A6 Reproducibility | Seed, dependency environment, data checksum, rerun instructions and observed successful clean execution |
| A7 Required documentation | Readable main PDF including CRISP-DM, properly labeled GPT/NotebookLM sections, 100 字以上 NotebookLM summary, external method comparison, plus a real GPT conversation PDF |
| A8 Packaging and safety | ID-named program and ZIP; required materials present; link/README provided for GitHub; no secrets; Git push and school submission excluded |

**Evaluation semantics:** no fabricated minimum R² or RMSE. A measured empirical conformal coverage not exactly equal to 95% is not alone a failure. Conditional or finite-sample coverage claims must be restricted to their justified assumptions. Verification must prove that calculations, data splits and reported outputs are correct, not merely present.

## 6. Non-goals
No Web App, FastAPI, database, full MLOps, forced Kaggle competition ranking when no ranking exists, or mandatory additional deep-learning or nonlinear models. No fake NotebookLM or GPT evidence. Do not silently convert reference-implementation behavior into new teacher requirements. 〔v0.2〕 **[R]** The CRISP-DM *Deployment* stage is met by a saved frozen predictor plus a documented prediction function that returns point and interval predictions. This is consistent with week05 and needs no service.

## 7. Remaining decisions / readiness checks
- ~~Dataset hard check~~ 〔v0.2〕 **Closed [F]:** CC0-1.0; 21,613 rows; 21 raw columns = 1 identifier + 1 target + 19 candidate source features (18 if `date` is dropped). Inside 10–20 under every defensible count (§10).
- **Q1** G2/G4 partition reading (§3 note).
- **Q2** Group-aware split for repeat sales.
- **Q3** Nested comparison protocol (§4.2).
- **Q4** Target and score scale for modeling and conformal (§4.3).
- **Q5** Student ID for the program and ZIP filenames (may be supplied before packaging; the placeholder is never a final filename).
- **Reporting handoff** (unchanged): real NotebookLM research and the authentic GPT chat export are collected by the acceptor; AI cannot manufacture usage evidence. 〔v0.2〕 **[R]** Because implementation will be done with Claude Code, the `GPT 輔助內容` section should name the tools actually used, while keeping the teacher's label.
- 〔v0.2〕 **File location [R]:** Bindings and `CLAUDE.md` place teacher documents in `doc/requirement/` and briefs in `doc/brief/`. These files are currently in `home_work_02/docs/`. Relocate them when the Outcome Contract is drafted.

## 8. Brief status and next step
〔v0.2〕 The dataset blocker is closed. The Brief is **ready to become an Outcome Contract draft** once Q1–Q4 are answered; Q5 can wait until packaging. Then: acceptor acceptance record → Design Authority lane decision (the expected multi-unit scope suggests Formal) → Spec derivation. Bindings §8.2 #3 still has the Fable alias probe pending. The acceptor decides whether that blocks the first formal audit.

## 9. 〔v0.2〕 Change log vs v0.1
| Section | Change |
|---|---|
| Header | Statement classes; governance path (Brief → Outcome Contract → DA Spec) |
| §2 | 100 字 reading; Kaggle-rank item N/A |
| §3 | G1–G8 verbatim; added G2/G4 reading note (Q1) |
| §4 | Steps 1–4 annotated; new §4.1 data facts, §4.2 comparison protocol, §4.3 conformal scope |
| §5 | A1, A3, A4, A5 evidence sharpened; no AC removed |
| §6 | Deployment interpretation added |
| §7 | Dataset check closed with evidence; Q1–Q5; tool-disclosure and file-location recommendations |
| §8 | Readiness restated |
| §10 | New: dataset verification evidence |

## 10. 〔v0.2〕 Dataset verification evidence [F]
Retrieved 2026-10-14 anonymously from the Kaggle public API (`api/v1/datasets/view|list|download/harlfoxem/housesalesprediction`) and inspected locally. The raw data was not added to the repository.

| Item | Value |
|---|---|
| Source | https://www.kaggle.com/datasets/harlfoxem/housesalesprediction — "House Sales in King County, USA", owner `harlfoxem`, datasetId 128 |
| License | CC0-1.0 |
| File | `kc_house_data.csv`, 2,515,206 bytes, Kaggle creationDate 2017-04-15 |
| Checksums | archive sha256 `1fdffaeec5e7656f6c09e29d9daa7e2157479c5f8e3a761758b4bfa43c773202`; CSV sha256 `d0875baa0251b21d4bdc9d2ae940a4fe0bb6009824f23dd0e2a5b2bf04557b7e` |
| Shape | 21,613 rows × 21 columns; no missing values; 0 duplicate rows; 21,436 unique `id` (177 repeat-sale rows) |
| Header | `id,date,price,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,grade,sqft_above,sqft_basement,yr_built,yr_renovated,zipcode,lat,long,sqft_living15,sqft_lot15` |
| Roles | identifier `id`; target `price`; candidate source features: `date` + 18 others listed in the header |
| Feature count | 19 with `date`, 18 without: both inside 10–20. Even if `id` were counted, 20 is still inside |
| Notable | `sqft_living = sqft_above + sqft_basement` in all rows; `price` US$75,000–7,700,000 (median 450,000); `zipcode` 70 values; date range 2014-05-02 → 2015-05-27 |
