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
            webserver_host = config['webserver-host']
    except FileNotFoundError:
        raise
    except IOError:
        raise

    app.root_path = os.getcwd()
    app.run(host=webserver_host, port=5050)
