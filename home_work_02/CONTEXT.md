# HW2 — Multiple Linear Regression (King County house prices)

This context defines the concepts used by HW2: predicting King County house sale prices with
linear-regression models under the CRISP-DM process, with feature selection, isolated evaluation
and conformal prediction intervals. Terms are framework-agnostic; implementation choices live in
the spec, not here.

## Sources

**Upper contract (上位契約)**:
The teacher's `HW2-requirements-Multiple Linear regression.txt`, which the MVM must fully satisfy.
Read-only for agents.
_Avoid_: The brief, the requirements (when the Grill Brief is meant)

**Grill Brief**:
The discussion draft (v0.1–v0.3) that records Grill decisions G1–G8 and clarifications C1–C4. It
feeds the Outcome Contract and has no authority of its own.
_Avoid_: The spec, the contract

## Data

**Sale**:
One row of `kc_house_data.csv`: one house sold on one date at one `price`.
_Avoid_: Record, sample (when the house is meant)

**House**:
The property identified by `id`; one house can have several sales (repeat sales).
_Avoid_: Listing, row

**Source feature**:
A raw CSV column other than the identifier `id` and the target `price`. The teacher's 10–20
feature rule counts source features.
_Avoid_: Feature (when an encoded column is meant), variable

**Encoded column**:
A model input column produced from source features by encoding or derivation; it does not count
toward the 10–20 rule.
_Avoid_: Feature, dummy feature (as a count)

## Partitions

**Fit partition**:
The 60% share of houses on which every model choice and every cross-validation happens.
_Avoid_: Training set, development set

**Calibration partition**:
The 20% share of houses used only to compute the conformal quantile of the frozen predictor.
_Avoid_: Validation set

**Test partition**:
The 20% share of houses evaluated once, after the predictor is frozen.
_Avoid_: Holdout (when Calibration is meant), validation set

**Development set**:
Fit plus Calibration (80%); the G2 wording for everything that is not Test.
_Avoid_: Training data (G2's "training data" means Fit)

## Modeling

**Candidate procedure**:
One compared approach — preprocessing, feature selection or hyperparameter choice, and fitting —
evaluated as a whole on the outer folds: all-features LR, forward LR, backward LR, Ridge, Lasso.
_Avoid_: Candidate model (a procedure produces a model per fold)

**Frozen predictor**:
The selected candidate procedure refit on the whole Fit partition, fixed before Calibration and
Test are used.
_Avoid_: Final model (ambiguous with outer-fold models), best model

**Prediction interval**:
The 95% split-conformal interval around a frozen-predictor prediction, calibrated on the log scale
and expressed in USD.
_Avoid_: Confidence interval (that is about a mean, not a single sale)
