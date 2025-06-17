APP_NAME=simple-offline-viewer
APP_ICON=app.icns

cd "$(dirname "$0")"

rm -R "dist/$APP_NAME" 2>/dev/null
rm -R "dist/$APP_NAME.app" 2>/dev/null

echo
echo '****************************************'
echo 'Running pyinstaller...'
echo '****************************************'

pyinstaller --noupx -w -i "$APP_ICON" -n "$APP_NAME" -D main.py --exclude-module _bootlocale --exclude-module PyQt5 --exclude-module PyQt6

echo
echo '****************************************'
echo 'Copying resources...'
echo '****************************************'

mkdir -p "dist/$APP_NAME.app/Contents/Resources/webroot"
cp -R resources/* "dist/$APP_NAME.app/Contents/Resources/webroot/"
mkdir -p "dist/$APP_NAME.app/Contents/Resources/webroot/tiles"

echo
echo '****************************************'
echo 'Creating ZIP...'
echo '****************************************'

cd dist
rm "$APP_NAME-macos.zip" 2>/dev/null
zip -q -r "$APP_NAME-standalone-macos-x64.zip" "$APP_NAME"
cd ..

echo
echo '****************************************'
echo 'Done.'
echo '****************************************'
echo
