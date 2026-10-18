"""Main seam for #62: ``methods`` (four path methods, k = 1…18) and complete ``winners`` in
``model_data`` (Spec rev 5 「`model_data` 契約」; G-2; #61 R1 F-2, F-3). Synthetic fixture only
(DA TR-01): the fixture runs the real selection code on synthetic rows, with one candidate
artificially invalidated (``hw2.fixture.inject_invalid_candidate``)."""
import copy

import pytest

from hw2 import contract, models, preprocess


def _entry(md, key):
    return contract.model_entries(md)[key]


def test_every_path_method_has_k_1_to_18_with_k_groups_everywhere(fixture_model_data):
    md, _ = fixture_model_data
    assert list(md["methods"]) == list(models.PATH_METHODS)
    n_folds = md["meta"]["cv"]["n_folds"]
    for method, items in md["methods"].items():
        assert [e["k"] for e in items] == list(range(1, 19))
        for e in items:
            assert len(e["canonical_groups"]) == e["k"]
            assert len(e["fold_groups"]) == n_folds == e["cv"]["n_folds"]
            assert all(len(g) == e["k"] for g in e["fold_groups"])
            assert set(e) == contract.ENTRY_KEYS
        last = items[-1]
        assert last["canonical_groups"] == list(preprocess.FEATURE_GROUPS)
    assert contract.test_field_paths(md["methods"]) == []
    assert set(md["meta"]["path_timing_s"]) == set(models.PATH_METHODS)
    assert set(md["meta"]["selection"]["methods"]) == set(models.PATH_METHODS)


def test_injected_invalid_candidate_is_marked_and_never_wins(fixture_run, fixture_model_data):
    md, _ = fixture_model_data
    key = fixture_run["injected_invalid"]
    assert key is not None and key.startswith("rfe_")
    entry = _entry(md, key)
    assert entry["status"]["state"] == "invalid" and entry["status"]["reason"]
    assert entry["cv"]["mean"] is None and not entry["is_method_winner"]
    assert key not in md["winners"]["authorized_test_models"] and key not in md["test"]
    assert md["winners"]["method_winners"]["rfe"]["model_key"] != key
    # the other candidates were evaluated as usual
    valid = [e for e in md["methods"]["rfe"] if e["status"]["state"] == "valid"]
    assert len(valid) == 17


def test_winners_are_recomputable_and_exclude_metric_only_models(fixture_model_data):
    md, _ = fixture_model_data
    w = md["winners"]
    for method, mw in w["method_winners"].items():
        valid = [e for e in md["methods"][method] if e["status"]["state"] == "valid"]
        best = min(valid, key=lambda e: (e["cv"]["mean"]["rmse"], e["k"]))
        assert mw["model_key"] == best["model_key"]
        assert [e["model_key"] for e in md["methods"][method] if e["is_method_winner"]] == \
            [best["model_key"]]
    pool = [("allin", md["baselines"]["allin"])] + [
        (m, _entry(md, w["method_winners"][m]["model_key"])) for m in models.PATH_METHODS]
    method, best = min(pool, key=lambda t: (t[1]["cv"]["mean"]["rmse"],
                                            models.METHOD_ORDER.index(t[0])))
    assert w["overall"]["model_key"] == best["model_key"] and w["overall"]["method"] == method
    # G-2: no Ridge/Lasso anywhere in the winners
    named = {mw["model_key"] for mw in w["method_winners"].values()}
    named |= {mw["test_model_key"] for mw in w["method_winners"].values()}
    named |= {w["overall"]["model_key"], w["overall"]["test_model_key"]}
    named |= set(w["authorized_test_models"])
    assert not named & {"ridge", "lasso"}
    assert set(w["method_winners"]) == set(models.PATH_METHODS)


def test_authorized_set_is_the_union_with_shared_models_once(fixture_model_data):
    md, _ = fixture_model_data
    w = md["winners"]
    union = ["allin"] + [mw["test_model_key"] for mw in w["method_winners"].values()] + \
        [w["overall"]["test_model_key"]]
    assert set(w["authorized_test_models"]) == set(union)
    subsets = [tuple(_entry(md, k)["canonical_groups"]) for k in w["authorized_test_models"]]
    assert len(set(subsets)) == len(subsets)
    for mw in w["method_winners"].values():
        assert _entry(md, mw["model_key"])["canonical_groups"] == \
            _entry(md, mw["test_model_key"])["canonical_groups"]


def _swap_winner(md, method, new_key):
    old = md["winners"]["method_winners"][method]["model_key"]
    _entry(md, old)["is_method_winner"] = False
    _entry(md, new_key)["is_method_winner"] = True
    md["winners"]["method_winners"][method].update(model_key=new_key, k=_entry(md, new_key)["k"])


def _break_nesting(md):
    e = md["methods"]["forward_sfs"][2]                     # k = 3, fold 0
    prev = set(md["methods"]["forward_sfs"][1]["fold_groups"][0])
    other = [g for g in preprocess.FEATURE_GROUPS if g not in prev][:3]
    e["fold_groups"][0] = other
    e["cv"]["folds"][0]["groups"] = other
    e["folds_agree"] = sum(g == e["canonical_groups"] for g in e["fold_groups"])


def _authorize_a_non_winner(md):
    """#61 R1 probe C1: a valid non-winner (another model) authorized and scored."""
    authorized = md["winners"]["authorized_test_models"]
    taken = {tuple(_entry(md, k)["canonical_groups"]) for k in authorized}
    extra = next(e for e in md["methods"]["forward_sfs"] if e["status"]["state"] == "valid"
                 and tuple(e["canonical_groups"]) not in taken)
    authorized.append(extra["model_key"])
    md["test"][extra["model_key"]] = {**copy.deepcopy(md["test"]["allin"]),
                                      "model_key": extra["model_key"]}


def _inflate_a_winner(md):
    """The recorded method winner no longer has the lowest CV RMSE (folds and mean consistent)."""
    method = next(m for m in models.PATH_METHODS if m != md["winners"]["overall"]["method"])
    e = _entry(md, md["winners"]["method_winners"][method]["model_key"])
    for f in e["cv"]["folds"]:
        f["rmse"] *= 10
    e["cv"]["mean"]["rmse"] *= 10


def _non_winner_valid_key(md, method):
    w = md["winners"]["method_winners"][method]["model_key"]
    return next(e["model_key"] for e in md["methods"][method]
                if e["status"]["state"] == "valid" and e["model_key"] != w)


@pytest.mark.parametrize("tamper, needle", [
    (lambda md: md["methods"]["rfe"].pop(), "k = 1"),
    (lambda md: md["methods"].__setitem__("ridge", copy.deepcopy(md["methods"]["rfe"])),
     "unknown path methods"),
    (_break_nesting, "exactly one group"),
    (lambda md: md["meta"]["cv"].__setitem__("n_folds", 4), "meta.cv.n_folds"),
    (lambda md: md["methods"]["lasso_path"][4].__setitem__("folds_agree", 99), "folds_agree"),
    (lambda md: md["methods"]["lasso_path"][4]["fold_groups"].pop(), "n_folds"),
    (lambda md: _swap_winner(md, "forward_sfs", _non_winner_valid_key(md, "forward_sfs")),
     "lowest CV RMSE"),
    (lambda md: _entry(md, _non_winner_valid_key(md, "lasso_path")).__setitem__(
        "is_method_winner", True), "flags differ"),
    (lambda md: md["winners"]["method_winners"].__setitem__(
        "ridge", {"model_key": "ridge", "k": 18, "cv_rmse": 1.0}), "G-2"),
    (lambda md: md["winners"]["overall"].update(
        model_key=md["winners"]["method_winners"]["rfe"]["model_key"], method="rfe",
        test_model_key=md["winners"]["method_winners"]["rfe"]["test_model_key"])
     if md["winners"]["overall"]["method"] != "rfe" else
     md["winners"]["overall"].update(model_key="allin", method="allin", test_model_key="allin"),
     "overall CV winner"),
    (lambda md: md["winners"]["method_winners"]["rfe"].__setitem__("test_model_key", "allin"),
     "different models"),
    (lambda md: [md["winners"]["authorized_test_models"].remove(k) or md["test"].pop(k)
                 for k in list(md["winners"]["authorized_test_models"]) if k != "allin"][:1],
     "not authorized|differs"),
    (lambda md: md["test"]["allin"].__setitem__("model_key", "forward_sfs_k01"), "model_key"),
    (_authorize_a_non_winner, "differs from All-in, the method winners"),
    (_inflate_a_winner, "lowest CV RMSE"),
])
def test_methods_and_winners_violations_are_rejected(fixture_model_data, tamper, needle):
    md = copy.deepcopy(fixture_model_data[0])
    contract.validate_model_data(md)
    tamper(md)
    with pytest.raises(contract.ContractError, match=needle):
        contract.validate_model_data(md)
