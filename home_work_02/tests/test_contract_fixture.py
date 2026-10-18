"""``test_inputs`` schema and the model_data writer, exercised with synthetic fixtures only
(DA TR-01: no official test row is loaded; fixture model_data never reaches official paths)."""
import copy

import pytest

from hw2 import contract, data, export, preprocess
from hw2.paths import MODEL_DATA_JS, MODEL_DATA_JSON


def _fixture_prepared(synthetic_csv):
    path, frame, sha = synthetic_csv
    return data.load_and_split(path, expected_sha256=sha, expected_rows=len(frame),
                               expected_unique_ids=frame["id"].nunique(), n_folds=3)


def _fixture_test_rows(synthetic_frame, prepared):
    """Synthetic rows standing in for test rows: positions and values of the synthetic frame."""
    rows = synthetic_frame.iloc[prepared.test_rows].copy()
    rows.insert(0, "row", prepared.test_rows)
    return rows


def test_fields_cover_identifiers_all_18_features_and_the_target():
    fields = contract.TEST_INPUT_FIELDS
    assert fields[:3] == ("row", "id", "date") and fields[-1] == "actual_price"
    assert set(preprocess.FEATURE_GROUPS) <= set(fields)
    assert len(fields) == 3 + 17 + 1
    assert "sqft_basement" not in fields and "price" not in fields


def test_empty_schema_is_valid_and_has_no_rows():
    obj = contract.empty_test_inputs()
    contract.validate_test_inputs(obj)
    assert obj["rows"] == [] and obj["written"] is False
    assert obj["n_houses"] is None and obj["n_repeat_sales"] is None


def test_fixture_rows_pass_the_schema(synthetic_csv, synthetic_frame):
    prepared = _fixture_prepared(synthetic_csv)
    rows = _fixture_test_rows(synthetic_frame, prepared)
    obj = contract.build_test_inputs(rows)
    contract.validate_test_inputs(obj, n_test=prepared.n_test)
    assert obj["n_rows"] == prepared.n_test
    assert obj["n_houses"] == rows["id"].nunique()
    assert obj["n_repeat_sales"] == len(rows) - rows["id"].nunique()
    first = dict(zip(obj["fields"], obj["rows"][0]))
    source = rows.sort_values("row").iloc[0]
    assert first["row"] == int(source["row"]) and first["id"] == source["id"]
    assert first["actual_price"] == source["price"] and first["zipcode"] == source["zipcode"]


def test_fixture_with_repeat_sales_counts_houses(synthetic_frame):
    rows = synthetic_frame.copy()
    rows.insert(0, "row", range(len(rows)))
    obj = contract.build_test_inputs(rows)
    assert obj["n_repeat_sales"] == 8 and obj["n_houses"] == 60


def _valid(synthetic_frame):
    rows = synthetic_frame.head(10).copy()
    rows.insert(0, "row", range(10))
    return contract.build_test_inputs(rows)


@pytest.mark.parametrize("tamper", [
    lambda o: o["rows"][0].pop(),
    lambda o: o["rows"][1].__setitem__(0, o["rows"][0][0]),
    lambda o: o["rows"][0].__setitem__(-1, 0),
    lambda o: o["rows"][0].__setitem__(contract.TEST_INPUT_FIELDS.index("zipcode"), "981"),
    lambda o: o["rows"][0].__setitem__(contract.TEST_INPUT_FIELDS.index("date"), "2014-01-01"),
    lambda o: o["rows"][0].__setitem__(contract.TEST_INPUT_FIELDS.index("grade"), "7"),
    lambda o: o.__setitem__("n_houses", o["n_houses"] + 1),
    lambda o: o.__setitem__("n_rows", 3),
    lambda o: o.__setitem__("fields", o["fields"][::-1]),
    lambda o: o.__setitem__("schema_version", 2),
])
def test_schema_violations_are_rejected(synthetic_frame, tamper):
    obj = _valid(synthetic_frame)
    tamper(obj)
    with pytest.raises(contract.ContractError):
        contract.validate_test_inputs(obj)


def test_row_count_must_equal_n_test(synthetic_frame):
    with pytest.raises(contract.ContractError, match="n_test"):
        contract.validate_test_inputs(_valid(synthetic_frame), n_test=11)


def test_unwritten_schema_with_rows_is_rejected(synthetic_frame):
    obj = _valid(synthetic_frame)
    obj["written"] = False
    with pytest.raises(contract.ContractError):
        contract.validate_test_inputs(obj)


def test_fixture_model_data_round_trips_through_json_and_js(tmp_path, synthetic_csv, synthetic_frame):
    prepared = _fixture_prepared(synthetic_csv)
    md = export.build_model_data(prepared, fixture=True)
    md["test_inputs"] = contract.build_test_inputs(_fixture_test_rows(synthetic_frame, prepared))
    json_path, js_path = export.write_model_data(md, tmp_path / "md.json", tmp_path / "md.js")
    import json
    from_json = json.loads(json_path.read_text(encoding="utf-8"))
    from_js = export.parse_js(js_path.read_text(encoding="utf-8"))
    assert from_json == from_js == json.loads(export.to_json(md))
    contract.validate_test_inputs(from_js["test_inputs"], n_test=prepared.n_test)
    assert from_js["meta"]["fixture"] is True


@pytest.mark.parametrize("target", ["json", "js"])
def test_fixture_model_data_is_refused_on_official_paths(tmp_path, synthetic_csv, target):
    prepared = _fixture_prepared(synthetic_csv)
    md = export.build_model_data(prepared, fixture=True)
    before = {p: (p.read_bytes() if p.exists() else None) for p in (MODEL_DATA_JSON, MODEL_DATA_JS)}
    kwargs = ({"json_path": MODEL_DATA_JSON, "js_path": tmp_path / "x.js"} if target == "json"
              else {"json_path": tmp_path / "x.json", "js_path": MODEL_DATA_JS})
    with pytest.raises(export.ExportError, match="official"):
        export.write_model_data(md, **kwargs)
    after = {p: (p.read_bytes() if p.exists() else None) for p in (MODEL_DATA_JSON, MODEL_DATA_JS)}
    assert before == after


def test_unmarked_model_data_is_treated_as_fixture(synthetic_csv):
    prepared = _fixture_prepared(synthetic_csv)
    md = export.build_model_data(prepared, fixture=False)
    del md["meta"]["fixture"]
    with pytest.raises(export.ExportError):
        export.write_model_data(md)


def test_writer_validates_test_inputs_against_n_test(tmp_path, synthetic_csv, synthetic_frame):
    prepared = _fixture_prepared(synthetic_csv)
    md = export.build_model_data(prepared, fixture=True)
    md["test_inputs"] = _valid(synthetic_frame)            # 10 rows, n_test differs
    assert prepared.n_test != 10
    with pytest.raises(contract.ContractError):
        export.write_model_data(md, tmp_path / "a.json", tmp_path / "a.js")


def test_parse_js_rejects_other_files():
    with pytest.raises(export.ExportError):
        export.parse_js("var x = 1;")


def test_meta_reports_the_fixture_split(synthetic_csv):
    prepared = _fixture_prepared(synthetic_csv)
    meta = copy.deepcopy(export.build_model_data(prepared, fixture=True)["meta"])
    assert meta["split"]["n_train"] == prepared.n_train
    assert meta["split"]["n_test"] == prepared.n_test
    assert meta["cv"]["n_folds"] == 3 and sum(meta["cv"]["fold_rows"]) == prepared.n_train
