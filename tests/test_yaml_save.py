import os
import pytest
import subprocess

from ..pygeoapi_config_dialog import PygeoapiConfigDialog


@pytest.mark.parametrize("sample_yaml", ["docker.config.yml"])
def test_json_schema(qtbot, sample_yaml: str):
    """Validate YAML against schema.json after loading and saving."""

    # Create the dialog widget and let qtbot manage it
    dialog = PygeoapiConfigDialog()
    qtbot.addWidget(dialog)

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
