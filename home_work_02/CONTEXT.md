# HW2 — Multiple Linear Regression (King County house prices)

This context defines the vocabulary of HW2: a CRISP-DM multiple-linear-regression analysis of
King County house sale prices with feature selection, model evaluation, 95% prediction intervals,
and a published interactive dashboard. Terms are framework-agnostic; implementation choices live in
the spec, not here.

## Sources

**Assignment page**:
The teacher's iLearning HW2 page (SRC-1 transcription, SRC-2 print, SRC-2T transcription, SRC-4
text copy of 2026-10-21). Its main text carries the formal requirements and, since SRC-4, the
bonus items; the 「補充」 section of SRC-2 carries suggestions.
_Avoid_: The spec, the brief

**Classroom Verbal Requirement**:
A requirement the teacher stated in class, confirmed by the acceptor, with no written source. The
dashboard delivery is one.
_Avoid_: Teacher document requirement (when no written text exists)

**Delivery example**:
SRC-3, the teacher's DIC-2 result site for 50 Startups. It shows the expected kind of result and
presentation, not the dataset, algorithms, or numbers to reproduce.
_Avoid_: Reference solution, template

## Data

**Sale**:
One row of the dataset: one house sold on one date at one `price`.
_Avoid_: Record, sample (when the house is meant)

**House**:
The property identified by `id`. A house can have several sales; all sales of a house stay on the
same side of every train/test and cross-validation split.
_Avoid_: Listing, row

**Source feature**:
A raw CSV column other than the identifier `id` and the target `price`, counted before any
categorical encoding. The teacher's feature-count rule counts source features.
_Avoid_: Feature (when an encoded column is meant), variable

**Encoded column**:
A model input column produced from source features by encoding or derivation. Encoded columns do
not count toward the feature-count rule.
_Avoid_: Feature, dummy feature (as a count)

**Training set**:
The share of the data on which every model choice, feature selection and hyperparameter tuning
happens, including cross-validation.
_Avoid_: Fit set, development set

**Test set**:
The share of the data held out and evaluated once, after every model choice is fixed.
_Avoid_: Validation set, holdout (when a CV fold is meant)

## Modeling

**Feature group**:
A source feature together with every encoded column derived from it (for example `zipcode` and
all its one-hot columns). Feature selection adds or removes whole groups; "k features" counts groups.
_Avoid_: Column set, dummy block

**Model rank**:
The number of linearly independent columns in the fitted design matrix, including the intercept. It,
not the feature count, sets the degrees of freedom for inference and Adjusted R².
_Avoid_: Number of features, number of parameters (when k is meant)

**All-in baseline**:
The single OLS model fitted on all 18 feature groups. It has no k path (it equals the k = 18
endpoint of the forward, backward and RFE paths), is shown as a reference line and one comparison
row, and competes for overall CV winner as itself.
_Avoid_: Full model (ambiguous with "the final model"), k = 18 method

**Feature-selection method**:
A procedure that ranks or chooses feature groups using only the rows it is given, yielding one
subset per feature count k. Run inside each cross-validation fold it yields that fold's subsets; run
on the whole training set it yields the canonical subsets.
_Avoid_: Model (a method yields subsets; a model is fitted on one subset)

**Canonical subset**:
For one method and one k, the subset computed on the whole training set. It is what the dashboard
shows, what the live predictor uses, and what is evaluated on the test set when it is a CV winner.
_Avoid_: The CV subset (fold subsets may differ), the selected features (ambiguous)

**CV winner**:
Two levels, both chosen among valid candidates by the lowest cross-validated RMSE (USD) on the
training set, before the test set is touched, and never changed by test results. A **method CV
winner** is the k whose canonical subset wins within one path method. The **overall CV winner** is
the single best of the four method CV winners and the All-in baseline; metric-only models do not
compete.
_Avoid_: Best model (ambiguous with the best test result), final model (until frozen)

**Test evaluation**:
The one-time scoring on the test set of each method's CV winner, the All-in baseline and the overall
CV winner (a model shared between these is scored once), reported descriptively. The Ridge and
Lasso comparison models are also scored once each, metric-only (USD MAE, MSE, RMSE, R²; no
interval, no coverage, no live prediction) and never compete for the overall CV winner. No other
model is scored on the test set, test results feed back into no selection, and nothing a dashboard
viewer does triggers a new scoring.
_Avoid_: Validation, benchmark

**Metric-only model**:
A comparison model (Ridge, Lasso) whose alpha is chosen by training CV and that reports CV and
one-time test metrics only. It has no prediction interval, no coverage and no live predictor.
_Avoid_: Candidate (it has no k path), baseline (reserved for All-in)

**Prediction interval**:
A 95% interval for a single new sale's price, with a stated statistical definition and an assumed
coverage that is verified empirically on the test set.
_Avoid_: Confidence interval (that is about the mean response), error band (an RMSE-width band is
not a prediction interval)

## Exploration

**Problem**:
One dataset together with the target it predicts, selectable on the dashboard. HW2 has two built-in
problems, King County house prices (the formal analysis) and 50 Startups profit (an exploratory
demonstration), plus any dataset a viewer supplies.
_Avoid_: Task, mode, example

**Formal analysis**:
The King County analysis performed by the main program: feature selection, CV winners, the one-time
test evaluation and the prediction intervals that the report and the dashboard's King County problem
show. Its numbers never change through the dashboard.
_Avoid_: Official model, production model

**Exploratory run**:
The on-the-spot preparation, feature selection, fitting and scoring that the dashboard performs in
the viewer's browser on a built-in demonstration problem or a viewer-supplied dataset. Its results
are recomputed on every run, are kept nowhere, enter no report, and are never a test evaluation.
_Avoid_: Test evaluation, live training, custom model

## Delivery

**Main program**:
The notebook `<學號>_hw2.ipynb`: the reproducible analysis across the six CRISP-DM phases and the
only source of the numbers the report and the dashboard show.
_Avoid_: Script, demo notebook

**Dashboard**:
The static interactive web page published on GitHub Pages under `home_work_02/`, driven by results
exported from the main program for the King County problem and by exploratory runs for the other
problems, and shipped in the submission package so that it works fully offline from `file://` with
no network and no server. Since the 2026-10-21 assignment page it is, with the repository, the
main delivery.
_Avoid_: Web app, backend, site (when the repository is meant), additional delivery

**Submission package**:
What is handed in on iLearning: the repository URL, the dashboard URL, and the ZIP
`<學號>_hw2.zip` containing the main program, the PDF report, the dashboard and the supporting
files.
_Avoid_: Release, deployment, the ZIP (when the links are meant too)
