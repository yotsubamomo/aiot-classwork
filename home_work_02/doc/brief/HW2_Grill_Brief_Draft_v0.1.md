# HW2 — House Price Prediction | Grill Brief Draft v0.1

**Status:** DISCUSSION DRAFT — not accepted, not an authoritative Spec, and no implementation authorization.
**Date:** 2026-10-14
**Source of authority:** Teacher's `HW2-requirements-Multiple Linear regression.txt` for coursework obligations; G1–G8 dialogue for proposed project choices. `multiple_linear_regression_crisp_dm.ipynb` is reference implementation only.

## 1. Outcome
Build a reproducible CRISP-DM analysis for predicting house prices from a Kaggle public dataset with 10–20 features. Compare multiple linear regression and selected alternatives with controlled feature selection, independent evaluation, and a prediction plot with uncertainty intervals. Deliver code, evidence, and the required PDF documentation and ZIP.

## 2. Teacher-required outcomes (unaltered in meaning)
- Kaggle public dataset with 10–20 features; name and source URL.
- Use linear regression for predictions; simple, multiple, or auto-regression may be attempted.
- Feature Selection and Model Evaluation must be performed.
- Prediction plot with a confidence interval **or** prediction interval.
- CRISP-DM: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment.
- Export all ChatGPT conversation as PDF with pdfCrowd or other means.
- Research web solutions to the same topic using NotebookLM, provide a **100+ character/word** summary as stated by the teacher (`100 字以上`) in the report, explicitly labeled `NotebookLM 摘要`.
- Explicitly label `GPT 輔助內容`; compare and explain mainstream or better internet solutions.
- Submit `7114056XXX_hw2.py/.ipynb`, PDF report, supporting files and directories packaged as `7114056XXX_hw2.zip` (replace placeholder with actual student ID).
- If GitHub is used or written in Colab, provide link and README describing workflow and results.
- Deadline shown: 2026-11-04. Assessment: documentation 50%, results 50%.

## 3. Confirmed Grill decisions (project additions)
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

## 4. Intended workflow and boundaries
1. Retrieve and pin exact Kaggle dataset version and record source, license, row count, raw column list, feature roles and target. Verify 10–20 source features **without treating one-hot expansion as a loophole**; document treatment of identifiers/date/zipcode.
2. Split deterministically into 60/20/20 disjoint Fit, Calibration, Test partitions. Keep Test inaccessible until model selection is frozen. Leakage-sensitive transformations and feature selection must be trained only in each applicable CV training fold within Fit.
3. Evaluate all-features linear regression, forward/backward-selected LR and Ridge/Lasso using comparable Fit-only 5-fold CV; select by CV RMSE with documented tie/secondary evaluation. Hyperparameters learned through the permitted Fit CV.
4. Freeze the chosen predictor; refit on Fit only; calibrate absolute residuals on Calibration using finite-sample conformal quantile (95% target) without tuning on Calibration. Assess test R², MAE, MSE, RMSE, marginal empirical coverage and mean interval width; show actual vs predicted with bounds and additional informative plots.
5. Produce notebook and report covering all six CRISP-DM stages, reproducibility, limitations, literature comparisons, source links, verified NotebookLM study and real GPT conversation export.
6. Package code, needed supporting data/metadata (subject to license), reports, requirements, and README into school-submission ZIP. Do not push or submit without separate human action.

## 5. Acceptance intent (draft; not authoritative ACs)
| Proposed AC | Observable evidence |
|---|---|
| A1 Dataset conforms | Original-source link, pinned copy/checksum or version, inspected raw header and feature count |
| A2 Analysis complete | Notebook and report cover six CRISP-DM stages and execute |
| A3 Isolation | Disjoint split assertions; fitted preprocessing/feature selection stays within Fit CV; calibration and test stay out of model tuning |
| A4 Core experiments | Repeatable comparison of baseline, forward/backward, Ridge and Lasso; CV RMSE and final holdout metrics |
| A5 Conformal interval | Tested finite-sample quantile logic, plot of values with lower/upper bound; test empirical coverage and mean width |
| A6 Reproducibility | Seed, dependency environment, data version, rerun instructions and observed successful clean execution |
| A7 Required documentation | Readable main PDF including CRISP-DM, properly labeled GPT/NotebookLM sections, 100 字以上 NotebookLM summary, external method comparison, plus real GPT conversation PDF |
| A8 Packaging and safety | ID-named program and ZIP; required materials present; link/README provided for GitHub; no secrets; Git push and school submission excluded |

**Evaluation semantics:** no fabricated minimum R²/RMSE; a measured empirical conformal coverage not exactly equal to 95% is not alone a failure. Conditional or finite-sample coverage claims must be restricted to their justified assumptions. Verification must prove that calculations, data splits, and reported outputs are correct, not merely present.

## 6. Non-goals
No Web App, FastAPI, database, full MLOps, forced Kaggle competition ranking when no ranking exists, or mandatory additional deep-learning/nonlinear models. No fake NotebookLM/GPT evidence. Do not silently convert reference-implementation behavior into new teacher requirements.

## 7. Remaining decisions / readiness checks
- **Dataset hard check:** validate exact Kaggle archive/CSV, license, target/features count and treatment of `id`, `date`, `zipcode`. If original source does not satisfy teacher constraint under a defensible count, return to Grill for dataset resolution.
- **Conformal scope:** final selected model is the primary interval target; whether plots/intervals are required for *every* compared model and which plot grouping is most readable should be decided when drafting verification semantics. State exchangeability assumptions and finite-sample conformal quantile rule.
- **Reporting handoff:** real NotebookLM research and authentic GPT chat export need collection and source indexing. AI cannot manufacture usage evidence.
- **Submission metadata:** actual student ID is not supplied; placeholder cannot be treated as a final filename.
- **Governance:** effective project governance/bindings and acceptance authority must be consulted before Brief acceptance, derivation and authorizing execution. Only the user can authorize reserved outside operations.

## 8. Brief status and next step
This draft is sufficient for **Brief review**, subject to the dataset hard check and any remaining choices above. It is not the approved Outcome Contract, formal Spec, Tickets, or implementation authorization.
