from tests.shared.utils import load_latest_output


def test_output_contains_scores(eval_dir):
    output = load_latest_output(eval_dir)
    assert "scores" in output, "Fehlendes 'scores'-Feld im Output"


def test_output_score_format(eval_dir):
    output = load_latest_output(eval_dir)
    assert isinstance(output["scores"], dict), "'scores' ist kein Dictionary"
    for key, value in output["scores"].items():
        assert isinstance(
            value, (int, float)
        ), f"Score '{key}' ist kein numerischer Wert"
