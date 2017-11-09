// Google map
var map;

// markers for map
var markers = [];

// info window
var info = new google.maps.InfoWindow();

$(function ()
{
	// styles for map
	// https://developers.google.com/maps/documentation/javascript/styling 	
	var styles = [
		// hide Google's labels
		{
			featureType : "all",
			elementType  : "labels",
			stylers : [
				{visibility : "off"}
			]
		},

		// hide roads
		{
			featureType : "road",
			elementType : "geometry",
			stylers : [
				{visibility : "off"}
			]
		}
	];

	// get DOM
	var canvas = $('#map-canvas').get(0);
	
	// options for map
	var options = {
		center : {lat : 12.972027, lng : 77.569597}, // Bangalore
		disableDefaultUI : true,
		mapTypeId : google.maps.MapTypeId.ROADMAP,
		maxZoom : 14,
		panControl : true,
		styles : styles,	
		zoom : 13,
		zoomControl : true
	};


	map = new google.maps.Map(canvas, options);
	
	// configure once loaded
	google.maps.event.addListenerOnce(map, "idle", configure);
});

/**
 * Configures application.
*/

function configure()
{
	// update UI after the map has been dragged 
	google.maps.event.addListener(map, "dragend", function() {
		// if info window isn't open
		if (!info.getMap || info.getMap())
		{
			update();
		}
	});

	// update UI after zoom level changes
	google.maps.event.addListener(map, "zoom_changed", function() {
		update();
	});

	// update UI
	update();
	// re-enable ctrl - and right-clicking (and thus Inspect Element) on the Google mmap
}
function removeMarkers()
{
	for (var i = 0; i < markers.length; i++)
	{
		markers[i].setMap(null);
	}
}

function addMarker(place)
{
	// set icons to be used
	var icon1 = {url : 'http://maps.google.com/mapfiles/kml/pal2/icon23.png', labelOrigin : {x : 17, y : 41}};
	var icon2 = {url : 'http://maps.google.com/mapfiles/kml/pal2/icon31.png', labelOrigin : {x : 17, y : 41}};

	// instantiate marker with help of place object
    	var i = markers.length;
	var position = {lat : place.latitude, lng : place.longitude};
	markers[i] = new google.maps.Marker ({
	    	position : position,
		map : map,
		icon : icon1,
		label : { text : place.place_name + ", " + place.admin_name1 }
    	});
}



function update()
{
	// get map bounds
	var bounds = map.getBounds();
	var ne = bounds.getNorthEast();
	var sw = bounds.getSouthWest();

	// get places within bounds asynchronously
	var parameters = {
		ne: ne.lat() + "," + ne.lng(),
		q: $("#q").val(),
		sw: sw.lat() + "," + sw.lng()
	};

	$.getJSON(Flask.url_for("update"), parameters)
	.done(function(data, textStatus, jqXHR) {
		
		// remove old markers
		removeMarkers();

		// add new markers to the map
		for (var i = 0; i < data.length; i++)
		{
			addMarker(data[i]);
		}
	})
	.fail(function(jqXHR, textStatus, errorThrown) {
		// log error into the browser console
		console.log(errorThrown.toString());
	});
};






















































