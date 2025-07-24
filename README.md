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

 ## Screenshot

![screenshot](/screenshot.png)

## Translate

1. Create or modify 'i18n\pygeoapi_config.pro' file to specify the .ui and .py files that contain translatable strings.

2. Run the following command from OSGeo4W Shell to generate .ts files specified in 'pygeoapi_config.pro':

`pylupdate5 i18n\pygeoapi_config.pro`

3. After editing the .ts files, run the following command to compile .dm files for each locale:

`lrelease pygeoapi_config_en_EN.ts`

## License

This project is released under an [MIT License](./LICENSE)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

