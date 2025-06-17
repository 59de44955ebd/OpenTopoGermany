# OpenTopoGermany

The actual purpose of this repository is not the code of the little demo app for Windows and macOS written in Python, but to provide the following [disk_images](https://github.com/59de44955ebd/OpenTopoGermany/releases/tag/disk_images) for download:

- [tiles_germany_otm_13.img.vhd.zip](https://github.com/59de44955ebd/OpenTopoGermany/releases/download/disk_images/tiles_germany_otm_13.img.vhd.zip) (1.95 GB) - [OpenTopoMap](https://opentopomap.org/) tiles of Germany 

- [tiles_germany_trails_13.img.vhd.zip](https://github.com/59de44955ebd/OpenTopoGermany/releases/download/disk_images/tiles_germany_trails_13.img.vhd.zip) (393 MB) - [Lonvia](https://github.com/waymarkedtrails) cycling and hiking trail overlay tiles of Germany

Both disk images are raw ".img" (dd) images with an additional VHD footer which also makes them valid .vhd files. Therfore they can be mounted directly both in Windows 10/11 and macOS simply by double-clicking them in Explorer resp. Finder (or by selecting "Mount..." from the context menu). To make the images macOS/Finder-compatible just remove the trailing ".vhd" from their filenames so that they have the extension ".img" instead. Finder/hdiutil doesn't mind the additional VHD footer and just ignores it.

The disk images have a FAT32 filesystem that contains downloaded/cached raster tiles (.png) for entire Germany up to zoom level 13 (which corresponds to about 1:50.000 in traditional paper maps). The tiles are meant for
usage in **webview-based but offline applications**, like e.g. a hiking (planning) app that also works when a user can't rely on a stable internet connection.

Map/tile providers generally don't like users to mass download tiles from their servers, but sometimes you have no other choice if the provider doesn't offer a complete dump e.g. as .zip file. So that's the purpose of this repository, to reduce the load of those providers. In addition, given the overhead of HTTP requests, downloading a single large image file is surely much more efficient than downloading hundreds of thousands individual .png files, so this also saves energy/climate.

## Demo app

"Simple Offline Viewer" is a simple and lightweight demo desktop application for Windows and macOS. It's written in Python and based on [pywebview](https://github.com/r0x0r/pywebview) and [Leaflet](https://leafletjs.com/).

Its purpose is to demonstrate how those disk images can be used in a desktop app. The app scans all mounted (virtual) disks/volumes and looks for a "tiles" directory directly in their root directory. If found, a subdirectory called "otm" is used for the base layer and subdirectories called "cycling" and "hiking" for the overlay layers. Obviously this could easily be extended to support additional base and overlay layers provided by other mounted disk images.

Usage:

- Mount "tiles_germany_otm_13.img.vhd" resp. "tiles_germany_otm_13.img", and optionally also "tiles_germany_trails_13.img.vhd" resp. "tiles_germany_trails_13.img".
- Run "simple-offline-viewer.exe" in Windows resp. "simple-offline-viewer.app" in macOS.
- If you mounted a disk image after starting the application, select "Reload" from the webview's context menu to make the application aware of the new offline tile source.

Features:

- View a topographic map of entire Germany without requiring an internet connection. This only requires the otm image to be mounted.
- If the trails image is also mounted, you can show/hide cycling and/or hiking trails using the control in the top right corner.
- Distances can be messured using the measure control in the top left corner.
- .gpx tracks can be loaded either by dropping them into the application window or clicking on the ".gpx" control.

## Screenshots

Demo app "Simple Offline Viewer" in Windows 11   
![](screenshots/viewer-windows-11.jpg)

Demo app "Simple Offline Viewer" in macOS 13   
![](screenshots/viewer-macos-13.jpg)

## ToDOs

OpenTopoMap shows a few more details in zoom level 14, but a corresponding tile disk image would require about 7.3 GB, and GitHub only allows up to 2 GB for each file attached to a release. Maybe I could split it into 4 separate parts that then have to be combined after the download.
