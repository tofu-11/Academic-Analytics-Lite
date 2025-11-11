from pathlib import Path
import json
import sys

BASE = Path(__file__).parent
CFG_PATH = BASE / "config.json"

# Default configuration. Users may edit config.json to override any value.
DEFAULTS = {
    "data_dir": "LMS Files",
    "file_extensions": [".csv"],
    "csv": {
        "encoding": "utf-8",
        "field_mapping": {
            "quiz1": "quiz_1",
            "quiz2": "quiz_2",
            "quiz3": "quiz_3",
            "quiz4": "quiz_4",
            "quiz5": "quiz_5",
            "midterm": "midterm",
            "final": "final_exam",
            "attendance_percent": "attendance"
        }
    },
    "grading": {
        # Weights should sum to 1.0 but code will normalize if they don't.
        "weights": {
            "quiz": 0.5,
            "midterm": 0.2,
            "final_exam": 0.2,
            "attendance": 0.1
        },
        "quiz_max_score": 20,
        "midterm_max_score": 100,
        "final_max_score": 100,
        "missing_data_policy": "mark_invalid"  # or 'treat_missing_as_zero'
    },
    "letter_grade_thresholds": {
        "S": 97,
        "A": 90,
        "B": 85,
        "C": 75,
        "D": 70,
        "F": 0
    }
}


def _deep_merge(a, b):
    result = dict(a)
    for k, v in (b or {}).items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def _write_sample_config(path: Path, defaults: dict):
    try:
        if not path.exists():
            path.write_text(json.dumps(defaults, indent=4))
    except Exception as exc:
        print(f"Warning: could not write sample config to {path}: {exc}", file=sys.stderr)


def _read_user_config(path: Path):
    if not path.exists():
        # create a sample config so users can edit it
        _write_sample_config(path, DEFAULTS)
        return {}

    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            print(f"Warning: {path} does not contain a JSON object; using defaults.", file=sys.stderr)
            return {}
        return data
    except json.JSONDecodeError as e:
        print(f"Warning: could not parse {path} (invalid JSON): {e}. Using defaults.", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Warning: unexpected error reading {path}: {e}. Using defaults.", file=sys.stderr)
        return {}


def _validate_config(cfg: dict):
    if not isinstance(cfg.get("data_dir", ""), str):
        print("Warning: 'data_dir' should be a string in config.json; falling back to default.", file=sys.stderr)

    exts = cfg.get("file_extensions")
    if exts is not None and (not isinstance(exts, list) or not all(isinstance(x, str) for x in exts)):
        print("Warning: 'file_extensions' should be a list of strings; falling back to default.", file=sys.stderr)

    csv = cfg.get("csv") or {}
    if not isinstance(csv, dict):
        print("Warning: 'csv' should be an object in config.json; falling back to default.", file=sys.stderr)
    else:
        fm = csv.get("field_mapping")
        if fm is not None and not isinstance(fm, dict):
            print("Warning: 'csv.field_mapping' should be an object/dict; falling back to default.", file=sys.stderr)

    grading = cfg.get("grading") or {}
    if not isinstance(grading, dict):
        print("Warning: 'grading' should be an object in config.json; falling back to default.", file=sys.stderr)
    else:
        weights = grading.get("weights")
        if weights is not None and (not isinstance(weights, dict) or not all(isinstance(v, (int, float)) for v in weights.values())):
            print("Warning: 'grading.weights' should be a dict of numeric values; falling back to default.", file=sys.stderr)


# Load and merge config
_user_cfg = _read_user_config(CFG_PATH)
CONFIG = _deep_merge(DEFAULTS, _user_cfg)
_validate_config(CONFIG)

__all__ = ["CONFIG"]
