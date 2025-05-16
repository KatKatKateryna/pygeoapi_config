# pygeoapi configurator

This plugin lets you read and write a [pygeoapi](https://pygeoapi.io/) configuration file on your local machine. 

## Deploy

copy this folder to your QGIS plugin directory. Something like:

 `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`

 ## Develop

 Install dependencies with:

 `pip install -r requirements`

 Compile resources with:

 `pb_tool compile`

Modify the user interface by opening pygeoapiconfig_dialog_base.ui in [Qt Creator](https://doc.qt.io/qtcreator/).
