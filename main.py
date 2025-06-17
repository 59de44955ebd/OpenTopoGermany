import os
import sys
import webview

APP_NAME = 'Simple Offline Viewer'

IS_WIN = sys.platform == 'win32'
IS_MAC = sys.platform == 'darwin'

if not IS_WIN and not IS_MAC:
    print('Sorry, Linux not supported yet.')
    sys.exit(1)

IS_FROZEN = getattr(sys, "frozen", False)

if IS_WIN:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    # In Windows there is no need for starting a web server, file URLs work perfectly fine
    START_URL = 'file:///' + os.path.join(APP_DIR, 'resources', 'index.htm')
else:
    if IS_FROZEN:
        APP_DIR = os.path.dirname(os.path.realpath(sys.executable))
        RES_DIR = os.path.realpath(os.path.join(APP_DIR, '..', 'Resources', 'webroot'))
    else:
        APP_DIR = os.path.dirname(os.path.realpath(__file__))
        RES_DIR = os.path.realpath(os.path.join(APP_DIR, 'resources'))
    START_URL = os.path.join(RES_DIR, 'index.htm')


class App():

    ########################################
    #
    ########################################
    def __init__(self, args=[]):

        class Api:

            def toggle_fullscreen(_):
                self.webview.toggle_fullscreen()

            def map_changed(_, zoom, lat, lng):
                self.webview.title = f'{APP_NAME} - map={zoom}/{lat}/{lng}'

        self.webview = webview.create_window(APP_NAME, START_URL, width=1024, height=768, js_api=Api())
        self.webview.events.loaded += self.find_tile_dirs

        if IS_MAC:
            def on_closed():
                for s in self.symlinks:
                    os.unlink(s)

            self.webview.events.closed += on_closed

    ########################################
    #
    ########################################
    def run(self):
        webview.settings['ALLOW_FILE_URLS'] = True
        if IS_WIN:
            webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False
        self.webview.events.before_load += lambda: webview.logger.setLevel('CRITICAL')
        webview.start(debug=True, server_args={'quiet': True})

    ########################################
    #
    ########################################
    def find_tile_dirs(self):
        if IS_WIN:
            for drive in os.listdrives():
                tiles_dir = (drive + 'tiles').replace('\\', '/')
                if os.path.isdir(tiles_dir):
                    for dir_name in os.listdir(tiles_dir):
                        self.webview.run_js(f"add_layer('{dir_name}', 'file:///{tiles_dir}/{dir_name}');")
        else:
            self.symlinks = []
            for vol in os.listdir('/Volumes'):
                tiles_dir = f'/Volumes/{vol}/tiles'
                if os.path.isdir(tiles_dir):
                    for dir_name in os.listdir(tiles_dir):
                        # To make tiles on mounted disk images accessible for the web server
                        # we have to create symbolic links in the local tiles dir
                        os.system(f'ln -s "{tiles_dir}/{dir_name}" "{RES_DIR}/tiles/{dir_name}" 2>/dev/null')
                        self.symlinks.append(f'{RES_DIR}/tiles/{dir_name}')
                        self.webview.run_js(f"add_layer('{dir_name}', 'tiles/{dir_name}');")


if __name__ == '__main__':
    app = App(sys.argv[1:])
    sys.exit(app.run())
