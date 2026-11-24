import json
import sys
from pathlib import Path

import jsonschema
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_money_flow as bmf  # noqa: E402


def write_totals(tmp_path, rows):
    investigation_dir = tmp_path / "investigations" / "some-slug"
    investigation_dir.mkdir(parents=True)
    (investigation_dir / "committee_totals.json").write_text(json.dumps(rows))
    return investigation_dir


def base_row(**overrides):
    row = {
        "committee_id": "C00000001",
        "committee_name": "TEST COMMITTEE",
        "cycle": 2026,
        "coverage_start_date": "2025-01-01",
        "coverage_end_date": "2026-06-30",
        "individual_itemized_contributions_usd": 1000.0,
        "individual_unitemized_contributions_usd": 50.0,
        "other_political_committee_contributions_usd": 25.0,
        "operating_expenditures_usd": 900.0,
        "contribution_refunds_usd": 10.0,
        "disbursements_usd": 950.0,
        "source": "FEC API, fetched directly 2026-10-03: https://api.open.fec.gov/v1/committee/C00000001/totals/",
    }
    row.update(overrides)
    return row


def test_real_generated_file_validates_against_schema():
    schema = json.loads((REPO_ROOT / "schemas" / "money_flow.schema.json").read_text())
    data = json.loads(
        (REPO_ROOT / "investigations" / "insight-housing-mvp-test" / "money_flow.json").read_text()
    )
    jsonschema.validate(data, schema)


def test_build_flow_output_always_validates(monkeypatch, tmp_path):
    investigation_dir = write_totals(tmp_path, [base_row()])
    monkeypatch.setattr(bmf, "REPO_ROOT", tmp_path)
    flow = bmf.build_flow("some-slug")
    schema = json.loads((REPO_ROOT / "schemas" / "money_flow.schema.json").read_text())
    jsonschema.validate(flow, schema)
    assert len(flow["edges"]) == 6


def test_negative_amount_is_skipped_not_emitted_negative(monkeypatch, tmp_path, capsys):
    write_totals(tmp_path, [base_row(contribution_refunds_usd=-50.25)])
    monkeypatch.setattr(bmf, "REPO_ROOT", tmp_path)
    flow = bmf.build_flow("some-slug")
    assert all(e["amount_usd"] >= 0 for e in flow["edges"])
    assert not any(e["flow_type"] == "refund" for e in flow["edges"])
    assert "negative" in capsys.readouterr().err


def test_null_operating_expenditures_does_not_crash(monkeypatch, tmp_path, capsys):
    write_totals(tmp_path, [base_row(operating_expenditures_usd=None)])
    monkeypatch.setattr(bmf, "REPO_ROOT", tmp_path)
    flow = bmf.build_flow("some-slug")
    other = [e for e in flow["edges"] if e["target_id"] == "category-other-disbursements"]
    assert len(other) == 1
    assert other[0]["amount_usd"] == 950.0
    assert "no operating_expenditures_usd" in capsys.readouterr().err


def test_missing_cycle_row_is_dropped_with_warning(monkeypatch, tmp_path, capsys):
    good = base_row()
    no_cycle = base_row(committee_id="C00000002")
    del no_cycle["cycle"]
    write_totals(tmp_path, [good, no_cycle])
    monkeypatch.setattr(bmf, "REPO_ROOT", tmp_path)
    flow = bmf.build_flow("some-slug")
    assert not any("c00000002" in n["id"] for n in flow["nodes"])
    assert "no 'cycle' field" in capsys.readouterr().err


def test_duplicate_committee_cycle_rows_are_deduped_not_summed(monkeypatch, tmp_path):
    early = base_row(source="FEC API, fetched directly 2026-07-01: https://api.open.fec.gov/v1/committee/C00000001/totals/")
    later = base_row(source="FEC API, fetched directly 2026-10-03: https://api.open.fec.gov/v1/committee/C00000001/totals/", operating_expenditures_usd=1234.0)
    write_totals(tmp_path, [early, later])
    monkeypatch.setattr(bmf, "REPO_ROOT", tmp_path)
    flow = bmf.build_flow("some-slug")
    opex_edges = [e for e in flow["edges"] if e["target_id"] == "category-operating-expenditures"]
    assert len(opex_edges) == 1
    assert opex_edges[0]["amount_usd"] == 1234.0


def test_unparseable_source_date_raises_instead_of_fabricating(monkeypatch, tmp_path):
    write_totals(tmp_path, [base_row(source="fetched recently: https://api.open.fec.gov/v1/committee/C00000001/totals/")])
    monkeypatch.setattr(bmf, "REPO_ROOT", tmp_path)
    with pytest.raises(SystemExit, match="accessed_date"):
        bmf.build_flow("some-slug")


def test_source_url_extraction_does_not_require_exact_label_colon_shape():
    text = "FEC bulk data download, 2026-09-15 (see https://api.open.fec.gov/v1/foo/ for detail)"
    assert bmf._extract_source_url(text) == "https://api.open.fec.gov/v1/foo/"


def test_missing_source_url_raises_instead_of_emitting_empty(monkeypatch, tmp_path):
    write_totals(tmp_path, [base_row(source="fetched directly 2026-10-03, no link given")])
    monkeypatch.setattr(bmf, "REPO_ROOT", tmp_path)
    with pytest.raises(SystemExit, match="source URL"):
        bmf.build_flow("some-slug")


def test_node_id_collision_with_conflicting_label_raises(monkeypatch, tmp_path):
    row_a = base_row(committee_id="C00000003", committee_name="FIRST NAME")
    row_b = base_row(committee_id="c00000003", committee_name="SECOND NAME", cycle=2024)
    write_totals(tmp_path, [row_a, row_b])
    monkeypatch.setattr(bmf, "REPO_ROOT", tmp_path)
    with pytest.raises(SystemExit, match="collision"):
        bmf.build_flow("some-slug")
