import os
from KodiMediaLibraryExplorer import app
import json

if __name__ == '__main__':
    try:
        with open("config.json") as f:
            config = json.load(f)
            webserver_host = config['webserver-host']
    except IOError:
        webserver_host = '127.0.0.1'

    app.root_path = os.getcwd()
    app.run(host=webserver_host, port=5050)
