var myCenter = new google.maps.LatLng(13.785520333, 100.569298833);
// var myCenter = new google.maps.LatLng(51.508742, -0.120850);

function initialize() {
	var mapProp = {
		center: myCenter,
		disableDefaultUI: true,
		zoom: 18,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

	var marker = new google.maps.Marker({
		position: myCenter,
		title: 'Click to zoom'
	});

	marker.setMap(map);

	// Zoom to 9 when clicking on marker
	google.maps.event.addListener(marker, 'click', function() {
		map.setZoom(9);
		map.setCenter(marker.getPosition());
	});

	google.maps.event.addListener(map, 'center_changed', function() {
		// 3 seconds after the center of the map has changed, pan back to the marker
		window.setTimeout(function() {
			map.panTo(marker.getPosition());
		}, 3000);
	});
}
google.maps.event.addDomListener(window, 'load', initialize);
</script>
<script type="text/javascript">
alert("Data: " + data + "\nStatus: " + status);
$("button").click(function() {
	$.get("demo_test.asp", function(data, status) {
		alert("Data: " + data + "\nStatus: " + status);
	});
});
