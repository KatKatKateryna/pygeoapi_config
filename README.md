![icon](/conf-icon.png)
# pygeoapi configurator

This plugin lets you read and write a [pygeoapi](https://pygeoapi.io/) configuration file on your local machine. You can deploy this configuration, by uploading it to a server with a pygeoapi instance.

In alternative you can pull and push a configuration directly from/to a running pygeoapi instance. In order to to this:

* The pygeoapi [admin API](https://docs.pygeoapi.io/en/latest/admin-api.html) must be enabled on that instance.
* The pygeoapi instance must be *unprotected* (*i.e.*: without authentication enabled).
* If you want to see the changes without restarting the service, you must [run pygeoapi with hot reload](https://docs.pygeoapi.io/en/latest/admin-api.html#pygeoapi-hot-reloading-in-gunicorn).

It goes without saying that a combination of an unprotected instance and an enabled admin API creates a security risk that is unaceptable for production scenarios. For that reason it should be used for **testing purposes only, without exposing the service to the Internet**.

Run pygeoapi docker container with hot reload, enabling the admin API:

```bash
docker run -p 5000:80 -e PYGEOAPI_SERVER_ADMIN=true geopython/pygeoapi:latest run-with-hot-reload
```

## Deploy

copy this folder to your QGIS plugin directory. Something like:

 `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`

 ## Develop

 Install dependencies with:

 `pip install -r requirements`

 Compile resources with:

 `pb_tool compile`

Modify the user interface by opening pygeoapiconfig_dialog_base.ui in [Qt Creator](https://doc.qt.io/qtcreator/).

 ## Run unit tests locally
 Run the following command from the root folder: 
 `python tests\run_tests_locally.py` 
 
 The YAML files to test against are stored under tests/yaml_samples and names as follows: 'organisation_repository_commit_filename'. 

 ## Screenshot

![screenshot](/screenshot.png)

## Translate

1. Create or modify 'i18n\pygeoapi_config.pro' file to specify the .ui and .py files that contain translatable strings.

2. Run the following command from OSGeo4W Shell to generate .ts files specified in 'pygeoapi_config.pro':

`pylupdate5 i18n\pygeoapi_config.pro`

3. After editing the .ts files, run the following command to compile .dm files for each locale:

`lrelease pygeoapi_config_pt.ts`

## Documentation

Build using:

` mkdocs build`

Test with live reload:

` mkdocs serve --livereload`

Deploy to `gh-pages` branch of your Github repository using

`mkdocs gh-deploy`

The original site is live at: https://pygeoapi-config.byteroad.net


## Contributing 🤝

This plugin is a live project and we welcome contributions from the community! If you have suggestions for improvements, found a bug, or want to add new features, feel free to:

* Open an [issue](https://github.com/opengeospatial/ogc-records-website/issues) to start a discussion
* Submit a [pull request](https://github.com/opengeospatial/ogc-records-website/pulls) with your proposed changes

We appreciate your support in making this plugin better!

## License

This project is released under an [MIT License](./LICENSE)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

