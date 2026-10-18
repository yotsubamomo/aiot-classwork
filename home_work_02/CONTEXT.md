# HW2 — Multiple Linear Regression (King County house prices)

This context defines the vocabulary of HW2: a CRISP-DM multiple-linear-regression analysis of
King County house sale prices with feature selection, model evaluation, 95% prediction intervals,
and a published interactive dashboard. Terms are framework-agnostic; implementation choices live in
the spec, not here.

## Sources

**Assignment page**:
The teacher's iLearning HW2 page (SRC-1 transcription, SRC-2 print, SRC-2T transcription). Its main
text carries the formal requirements; its 「補充」 section carries suggestions.
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
The feature subset (and, overall, the method) with the lowest cross-validated RMSE on the training
set. It is chosen before the test set is touched and is not changed by test results.
_Avoid_: Best model (ambiguous with the best test result), final model (until frozen)

**Test evaluation**:
The one-time scoring on the test set of each method's CV winner, the All-in baseline and the overall
CV winner (a model shared between these is scored once), reported descriptively. No other model is
scored on the test set, and nothing a dashboard viewer does triggers a new one.
_Avoid_: Validation, benchmark

**Prediction interval**:
A 95% interval for a single new sale's price, with a stated statistical definition and an assumed
coverage that is verified empirically on the test set.
_Avoid_: Confidence interval (that is about the mean response), error band (an RMSE-width band is
not a prediction interval)

## Delivery

**Main program**:
The notebook `<學號>_hw2.ipynb`: the reproducible analysis across the six CRISP-DM phases and the
only source of the numbers the report and the dashboard show.
_Avoid_: Script, demo notebook

**Dashboard**:
The static interactive web page published on GitHub Pages under `home_work_02/`, driven by results
exported from the main program, and shipped in the submission package so that it works fully
offline from `file://` with no network and no server. An additional delivery; it replaces none of
the assignment page's required files.
_Avoid_: Web app, backend, site (when the repository is meant)

**Submission package**:
The ZIP `<學號>_hw2.zip` uploaded to iLearning, containing the main program, the PDF report and
the supporting files the assignment page requires.
_Avoid_: Release, deployment
