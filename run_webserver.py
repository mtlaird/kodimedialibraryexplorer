import argparse
import os
from KodiMediaLibraryExplorer import app
import json

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", "-c")

    args = parser.parse_args()
    clean_args = {k: v for k, v in vars(args).items() if v is not None}
    config_file = clean_args["config_file"] if "config_file" in clean_args else "config.json"

    try:
        with open(config_file) as f:
            config = json.load(f)
            for key in config:
                app.config[key] = config[key]
    except FileNotFoundError:
        raise
    except IOError:
        raise

    if "root-path" in app.config:
        app.root_path = app.config["root-path"]
    else:
        app.root_path = os.getcwd()
    app.run(host=app.config["webserver-host"], port=5050)
