import json
from pathlib import Path

import generate_report


FIXTURES = Path(__file__).parent / "fixtures"


def load_report_data():
    return json.loads((FIXTURES / "report_data.json").read_text(encoding="utf-8"))


def test_scoring_config_loads_weights_from_resource_file():
    config = generate_report.load_scoring_config()
    weights = generate_report.get_scoring_weights(config)

    assert weights["pagespeed"] == 15
    assert "llms_txt" not in weights
    assert sum(weights.values()) == 100


def test_calculate_overall_score_uses_config_weights():
    data = load_report_data()
    scores = generate_report.calculate_overall_score(data)

    assert scores["weights"]["broken_links"] == 10
    assert scores["categories"]["security"] == 75
    assert scores["categories"]["pagespeed"] == 57
    assert 0 <= scores["overall"] <= 100


def test_markdown_report_contains_score_card_and_findings():
    data = load_report_data()
    scores = generate_report.calculate_overall_score(data)

    markdown = generate_report.render_markdown_report(data, scores)

    assert "# Full Audit Report" in markdown
    assert "| Performance and Core Web Vitals | 15 | 57 |" in markdown
    assert "Content-Security-Policy is missing" in markdown
    assert "Score confidence: `High`" in markdown
    assert "No llms.txt found" not in markdown


def test_missing_llms_txt_is_informational_and_does_not_change_score():
    data = load_report_data()
    without_file = generate_report.calculate_overall_score(data)
    data["sections"]["llms_txt"] = {
        "exists": True,
        "quality": {"score": 100, "issues": [], "suggestions": []},
    }
    with_file = generate_report.calculate_overall_score(data)

    assert without_file["overall"] == with_file["overall"]
    assert "llms_txt" not in without_file["weights"]
    assert all(fix["title"] != "No llms.txt found" for fix in generate_report.build_environment_fixes(data))


def test_action_plan_prioritizes_findings_and_pagespeed_opportunities():
    data = load_report_data()
    scores = generate_report.calculate_overall_score(data)

    action_plan = generate_report.render_action_plan(data, scores)

    assert "# Action Plan" in action_plan
    assert "Content-Security-Policy is missing" in action_plan
    assert "Eliminate render-blocking resources" in action_plan


def test_write_text_output_creates_parent_directories(tmp_path):
    output = tmp_path / "nested" / "FULL-AUDIT-REPORT.md"

    written = generate_report.write_text_output(str(output), "# Report\n")

    assert Path(written).is_file()
    assert output.read_text(encoding="utf-8") == "# Report\n"
