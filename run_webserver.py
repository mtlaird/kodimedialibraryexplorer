import os
from KodiMediaLibraryExplorer import app


if __name__ == '__main__':
        app.root_path = os.getcwd()
        app.run(host='192.168.77.71', port=5050)
