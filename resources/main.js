'use strict';

// Arbitrary defaults (Berlin)
let zoom = 12,
    lat = 52.51350476109457,
    lng = 13.409671783447267;

const map = L.map('map', {
	editable: true,
    layers: [],
    wheelPxPerZoomLevel: 240,
	contextmenu: true,
	contextmenuItems: [
	{
	    text: 'Center map here',
	    callback: (e) => map.panTo(e.latlng),
	},
	'-',
	{
	    text: 'Reload Page',
	    callback: () => {location.reload();},
	},
	]
})

const layers_control = L.control.layers([], {}, {position: 'topright'});

L.control.scale().addTo(map);

L.control.measure({position: 'topleft'}).addTo(map);

function map_changed()
{
    const p = map.getCenter();
    window.pywebview.api.map_changed(map.getZoom(), p.lat, p.lng);
}

const style_track = {color: '#ee0033', opacity: 0.6, weight: 3, clickable: false};
L.Control.FileLayerLoad.LABEL = 'gpx';
var fileL = L.Control.fileLayerLoad({
    fileSizeLimit: 1024 * 1024 * 10,
	fitBounds: true,
	layerOptions: {
		style: style_track,
		pointToLayer: function (data, latlng) {
			return L.circleMarker(latlng, {style: style_track});
		}
	},
}).addTo(map);

fileL.loader.on('data:loaded', function (e){
	layersControl.addOverlay(e.layer, e.filename);
});

map.setView([lat, lng], zoom);

map.on('moveend', function(evt) {
	map_changed();
});

window.addEventListener('pywebviewready', () => {
	map_changed();
	window.addEventListener('keydown', (e) => {
		if (e.keyCode == 122)
			window.pywebview.api.toggle_fullscreen();
	});
});

let layers_control_added = false;

function add_layer(name, path, maxNativeZoom, is_base)
{
	if (is_base)
	{		
		map.addLayer(
			L.tileLayer(
				path + '/{z}/{x}/{y}.png',
			    {
			    	maxNativeZoom: maxNativeZoom,
			        maxZoom: 20,
			    }
			),
			name.charAt(0).toUpperCase() + name.slice(1)
		);
	}
	else
	{
		layers_control.addOverlay(
			L.tileLayer(
				path + '/{z}/{x}/{y}.png',
			    {
			    	maxNativeZoom: maxNativeZoom,
			        maxZoom: 20,
			    }
			),
			name.charAt(0).toUpperCase() + name.slice(1)
		);
		if (!layers_control_added)
		{
			layers_control.addTo(map);
			layers_control_added = true;
		}
	}
}
