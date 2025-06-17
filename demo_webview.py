import subprocess
import time
from winapp.mainwin import *
from winapp.dlls import *
from winapp.custom_controls.webview import *
from winapp.controls.statusbar import *

APP_NAME = 'Webbrowser Demo'
APP_DIR = os.path.dirname(os.path.abspath(__file__))

IDM_EXIT = 100
IDM_ABOUT = 101

START_URL = 'file:///' + os.path.join(APP_DIR, 'resources', 'index.htm')

menu_data = {
    "items": [
        {
            "caption": "&File",
            "items": [
                {
                    "caption": "E&xit",
                    "id": IDM_EXIT
                },
            ]
        },
        {
            "caption": "&Help",
            "items": [
                {
                    "caption": f"&About\tF1",
                    "id": IDM_ABOUT
                },
            ]
        }
    ]
}


class App(MainWin):

    def __init__(self, args=[]):

#        vhd_files = [os.path.join(APP_DIR, f) for f in os.listdir(APP_DIR) if f.lower().endswith('.vhd')]  # and if os.path.isfile(os.path.join(APP_DIR, f))
#        if vhd_files:
##            num_drives = sum([1 for i in range(ord('A'), ord('Z') + 1) if os.path.isdir(chr(i)+':')])
#            num_drives = len(os.listdrives())
#            for vhd in vhd_files:
#                print(f'Trying to mount {vhd}...')
#                # Using explorer to mount
#                # Pro: no elevation needed (as opposed to using diskpart)
#                # Con: no control/feedback, new explorer window pops up
#                subprocess.run(['explorer.exe', vhd], shell=False)
#                # Wait up to 2.5 sec. for a new drive letter to appear
#                for i in range(10):
#                    time.sleep(.2)
##                    num_drives_new = sum([1 for i in range(ord('A'), ord('Z') + 1) if os.path.isdir(chr(i)+':')])
#                    num_drives_new = len(os.listdrives()) 
#                    if num_drives_new > num_drives:
#                        num_drives = num_drives_new    
#                        break
                        
        self.COMMAND_MESSAGE_MAP = {
            IDM_EXIT:                   self.quit,
            IDM_ABOUT:                  self.action_about,
        }

        ########################################
        # Create main window
        ########################################
        super().__init__(
            APP_NAME,
            style=WS_OVERLAPPEDWINDOW,# | WS_HSCROLL | WS_VSCROLL,
            width=1024, height=768,
            class_style=0,
            menu_data=menu_data,
        )

        ########################################
        # Create StatusBar
        ########################################
        self.statusbar = StatusBar(self)

        self.apply_theme(True)
        
        self.show()
                        
        ########################################
        # Create WebBrowser control
        ########################################
        rc = self.get_client_rect()
        self.webview = WebView(
            self,
            width=rc.right,
            height=rc.bottom - self.statusbar.height,
            debug=True
        )
        
        ########################################
        #
        ########################################
        def on_load(id, args):
            self.find_tile_dirs()
            
#            self.webview.js_eval('''
#            document.body.addEventListener("dragover", (e) => {
#              e.preventDefault();
#              return false;
#            });
#            document.body.addEventListener("dragleave", (e) => {
#              e.preventDefault();
#              return false;
#            });
#            document.body.addEventListener("drop", (e) => {
#              e.preventDefault();
#              console.log(e.dataTransfer.files[0]);
#            })''')
#            
        self.webview.js_bind('__onload__', on_load)
        
        self.webview.navigate(START_URL)
        self.webview.set_focus()

        ########################################
        #
        ########################################
        def _on_WM_SIZE(hwnd, wparam, lparam):
            #self.toolbar.update_size()
            self.statusbar.update_size()

            # Resize control container (AtlAxWin) to window
            width, height = lparam & 0xFFFF, (lparam >> 16) & 0xFFFF
            height -= self.statusbar.height
            self.webview.set_window_pos(width=width, height=height, flags=SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE)

        self.register_message_callback(WM_SIZE, _on_WM_SIZE)
        
        ########################################
        #
        ########################################
        def _on_WM_COMMAND(hwnd, wparam, lparam):
            if lparam == 0:
                command_id = LOWORD(wparam)
                if command_id in self.COMMAND_MESSAGE_MAP:
                    self.COMMAND_MESSAGE_MAP[command_id]()
                    return FALSE

            return FALSE

        self.register_message_callback(WM_COMMAND, _on_WM_COMMAND)
        
    ########################################
    #
    ########################################
    def find_tile_dirs(self):
        self._tile_dirs = []
        for i in range(ord('A'), ord('Z') + 1):
            root = f'{chr(i)}:\\tiles'
            if os.path.isdir(root):
                for d in os.listdir(root):
                    self.webview.js_eval(f"add_layer('{d}', '{chr(i)}');")
                            
    ########################################
    # 
    ########################################
    def action_about(self):
        msg = 'Map Demo v0.1\n(c) 2025 59de44955ebd\n\nA simple map viewer based on Python 3,\nWebView2 and Leaflet.'
        self.show_message_box(msg, 'About')
        
    ########################################
    # IMPORTANT!
    ########################################
    def run(self):
        self.webview.run()


if __name__ == '__main__':
    app = App(sys.argv[1:])
    sys.exit(app.run())
