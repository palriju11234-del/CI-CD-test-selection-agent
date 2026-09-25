import json

from app.ml.fever_loader import load_fever_dataset


def test_load_fever_dataset_maps_supported_labels_and_skips_unknown(tmp_path):
	data_path = tmp_path / "fever.jsonl"
	records = [
		{"claim": "supported claim", "label": "SUPPORTS"},
		{"claim": "refuted claim", "label": "REFUTES"},
		{"claim": "unknown claim", "label": "UNKNOWN"},
	]
	data_path.write_text(
		"\n".join(json.dumps(record) for record in records),
		encoding="utf-8",
	)

	dataframe = load_fever_dataset(str(data_path))

	assert dataframe.to_dict("records") == [
		{"claim": "supported claim", "label": "true"},
		{"claim": "refuted claim", "label": "false"},
	]