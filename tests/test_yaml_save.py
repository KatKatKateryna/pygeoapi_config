import os
import pytest
import subprocess

from ..pygeoapi_config_dialog import PygeoapiConfigDialog


@pytest.fixture()
def base_dir():
    return os.path.dirname(os.path.abspath(__file__))  # directory of current file


@pytest.mark.parametrize(
    "sample_yaml",
    ["docker.config.yml", "pygeoapi-test-config-ogr.yml", "cite.config.yml"],
)
def test_json_schema_on_open_save(qtbot, base_dir, sample_yaml: str):
    """Validate YAML against schema.json after loading and saving."""

    # Create the dialog widget and let qtbot manage it
    dialog = PygeoapiConfigDialog()
    qtbot.addWidget(dialog)

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
    print(f"_______File saved as '{abs_new_yaml_path}'", flush=True)
    assert result.returncode == 0, f"Validation failed:\n{result.stderr}"


@pytest.mark.parametrize(
    "sample_yaml",
    ["docker.config.yml", "pygeoapi-test-config-ogr.yml", "cite.config.yml"],
)
def test_open_file_validate_ui_data(qtbot, base_dir, sample_yaml: str):
    """Run UI data validation from opened file (done in the plugin before saving to the new file)."""

    # Create the dialog widget and let qtbot manage it
    dialog = PygeoapiConfigDialog()
    qtbot.addWidget(dialog)

    # Load YAML
    abs_yaml_path = os.path.join(base_dir, sample_yaml)
    dialog.open_file(abs_yaml_path)  # now dialog.config_data has the data stored

    # Validate UI data (to follow exactly the user experience after clicking Save button)
    data_valid, invalid_props = dialog._set_validate_ui_data()
    if not data_valid:
        # 2 sample files are expected to fail the UI validation (incomplete "Hello" Resource data)
        # only fail the test if a legit file ("docker.config.yml") did not pass the validation
        if sample_yaml == "docker.config.yml":
            assert False, f"'{sample_yaml}' file UI data is not valid: {invalid_props}"

    print(f"_________Data validated for '{sample_yaml}'", flush=True)
    assert True
