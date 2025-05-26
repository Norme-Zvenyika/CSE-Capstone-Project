"""
shared resources for transform package

- loads name_mappings.json once and exposes:
    - default_utility_providers_mapping
    - default_suppliers_names_mapping
    - rate_type_mapping
- provides BaseTransform interface that every year-range transform must implement
"""

import json
from pathlib import Path

# adjust this if the file lives elsewhere or inject the path via env var
MAPPINGS_PATH = Path(__file__).parent / "name_mappings.json"
if not MAPPINGS_PATH.exists():
    raise FileNotFoundError(f"name_mappings.json not found at {MAPPINGS_PATH}")

def _load_mappings(path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as err:
        raise FileNotFoundError(f"name mappings file not found: {path}") from err
    except json.JSONDecodeError as err:
        raise ValueError(f"invalid JSON in name mappings file: {path}") from err

_name_mappings = _load_mappings(MAPPINGS_PATH)

default_utility_providers_mapping = _name_mappings["default_utility_providers_mapping"]
default_suppliers_names_mapping  = _name_mappings["default_suppliers_names_mapping"]
rate_type_mapping               = _name_mappings["rate_type_mapping"]

class BaseTransform:
    """interface each year-range transform class must implement"""
    def transform(self, data):
        raise NotImplementedError
