import pytest
from copy import deepcopy
from unittest.mock import MagicMock, patch

from ..utils.data_diff import diff_yaml_dict_remove_known_faulty_fields
from ..pygeoapi_config_dialog import PygeoapiConfigDialog

# Important: get your pygeoapi instance up & running, first!
# docker run -p 5000:80 -v $(pwd)/example-config.yml:/pygeoapi/local.config.yml geopython/pygeoapi:latest run-with-hot-reload
# Double check the SERVER_URL is correct

SERVER_URL = "http://localhost:5000/admin/config"


@pytest.fixture
def dialog(qtbot):
    """Fixture to create the dialog"""

    dialog = PygeoapiConfigDialog()
    qtbot.addWidget(dialog)

    dialog.update_config_data_and_ui = MagicMock()

    return dialog


@patch("pygeoapi_config.pygeoapi_config_dialog.QgsMessageLog", create=True)
@patch("pygeoapi_config.pygeoapi_config_dialog.QMessageBox")
def test_pull_then_push_config(mock_msgbox, mock_log, dialog):
    """Pull config data from server, then push it back."""

    print(f"Pulling data from: {SERVER_URL}", flush=True)

    dialog.pull_from_server(SERVER_URL)

    if mock_msgbox.critical.called:
        error_call = mock_msgbox.critical.call_args[0][2]
        pytest.fail(f"Pull operation failed: {error_call}")

    assert (
        dialog.update_config_data_and_ui.called
    ), "update_config_data_and_ui was never called after pull"

    # Get the data that was pulled
    yaml1_data = dialog.config_data.asdict_enum_safe(
        deepcopy(dialog.yaml_original_data), datetime_to_str=False
    )
    print("___________________________________________YAML1:", flush=True)
    print(yaml1_data, flush=True)

    print("___________________________________________Args:", flush=True)
    print(dialog.update_config_data_and_ui.call_args[0], flush=True)
    pulled_data = dialog.update_config_data_and_ui.call_args[0][0]

    print("___________________________________________Pulled data:", flush=True)
    print(pulled_data, flush=True)
    assert isinstance(pulled_data, dict)
    print(f"Successfully config data: {list(pulled_data.keys())}", flush=True)

    # Reset mock call history
    mock_msgbox.information.reset_mock()
    mock_msgbox.critical.reset_mock()

    print("___________________________________________URL:", flush=True)
    print(SERVER_URL, flush=True)
    print(f"Pushing data back to: {SERVER_URL}", flush=True)
    dialog.push_to_server(SERVER_URL, pulled_data)

    print("___________________________________________Args2:", flush=True)
    print(mock_msgbox.information.call_args_list, flush=True)
    # Check if push failed
    if mock_msgbox.critical.called:
        error_call = mock_msgbox.critical.call_args[0][2]
        pytest.fail(f"Push operation failed: {error_call}")

    success = False
    for call in mock_msgbox.information.call_args_list:
        if "Success! Status Code: 204" in call[0][2]:
            success = True
            break

    assert success, "Success message box was not triggered after push"
    print("Roundtrip Complete: Data pulled and pushed successfully.", flush=True)

    # Pull again and get the data to compare
    dialog.pull_from_server(SERVER_URL)

    yaml2_data = dialog.config_data.asdict_enum_safe(
        deepcopy(dialog.yaml_original_data), datetime_to_str=False
    )

    yaml1_missing_props = None

    diff_data = diff_yaml_dict_remove_known_faulty_fields(
        yaml1_data, yaml2_data, yaml1_missing_props
    )

    if (
        len(diff_data["added"]) + len(diff_data["removed"]) + len(diff_data["changed"])
        == 0
    ):
        assert True
        print(f"No changes detected after the push to: '{SERVER_URL}'.", flush=True)
        return

    assert (
        False
    ), f"YAML data changed after pushing to: '{SERVER_URL}'. \nAdded: {len(diff_data['added'])} fields, changed: {len(diff_data['changed'])} fields, removed: {len(diff_data['removed'])} fields."
