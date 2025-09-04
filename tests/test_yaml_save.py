import os
import pytest
from PyQt5.QtWidgets import QApplication
import subprocess

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pygeoapi_config_dialog import PygeoapiConfigDialog


@pytest.fixture(scope="session")
def qapp():
    """Ensure a QApplication exists for all tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.mark.parametrize("sample_yaml", ["docker.config.yml"])
def test_json_schema(sample_yaml: str):
    """Validate YAML against schema.json after loading and saving."""

    dialog = PygeoapiConfigDialog()
    base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of current file

    # Load YAML
    abs_yaml_path = os.path.join(base_dir, sample_yaml)
    dialog.open_file(abs_yaml_path)  # now dialog.config_data has the data stored

    # Save YAML
    new_yaml_name = f"saved_{sample_yaml}"
    abs_new_yaml_path = os.path.join(base_dir, new_yaml_name)
    dialog.save_to_file(abs_new_yaml_path)

    result = subprocess.run(
        [
            "check-jsonschema",
            "--schemafile",
            "https://raw.githubusercontent.com/geopython/pygeoapi/refs/heads/master/pygeoapi/resources/schemas/config/pygeoapi-config-0.x.yml",
            abs_new_yaml_path,
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Validation failed:\n{result.stderr}"
