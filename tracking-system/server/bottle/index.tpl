<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>D3: Adding and removing values from a chart (dynamic labels included)</title>
<!--	<script type="text/javascript" src="../d3/d3.v3.js"></script> -->
	<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"></script>
	<script src="http://maps.google.com/maps/api/js?sensor=false"></script>
	<style type="text/css">
		.inline {
			float: left;
			padding-right: 20px;
		}
		svg {
			font: 10px sans-serif;
		}
		.line {
			fill: none;
			stroke: #000;
			stroke-width: 1.5px;
		}
		.axis path,
		.axis line {
			fill: none;
			stroke: #000;
			shape-rendering: crispEdges;
		}
	</style>
</head>
<body>
	<div id="map" class="inline">
		<div id="googleMap" style="width:500px;height:380px;"></div>
		<div>
			<button>Click Me</button>
		</div>
	</div>
	<div id="graph" class="inline"></div>
	<script type="text/javascript">

/****************************************************************************
* Google Map
*/

var myCenter = new google.maps.LatLng(13.785520333, 100.569298833);
// var myCenter = new google.maps.LatLng(51.508742, -0.120850);

function initialize() {
	var mapProp = {
		center: myCenter,
		disableDefaultUI: true,
		zoom: 17,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	// var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

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
alert("Data: " + data + "\nStatus: " + status);

$("button").click(function() {
	$.get("demo_test.asp", function(data, status) {
		alert("Data: " + data + "\nStatus: " + status);
	});
});

	</script>
	<script type="text/javascript">

/****************************************************************************
*	Graph
*/
function tick() {

	// push a new data point onto the back
	data.push(random());

	// redraw the line, and slide it to the left
	path.attr("d", line)
		.attr("transform", null)
		.transition()
		.duration(500)
		.ease("linear")
		.attr("transform", "translate(" + x(-1) + ",0)")
		.each("end", tick);

	// pop the old data point off the front
	data.shift();
}

// var n = 80,
	// random = d3.random.normal(0, .2),
// 	data = d3.range(n).map(random);
var n = 80;
var random = d3.random.normal(0, .2);
var data = [ {{ data }} ];

var margin = {top: 20, right: 20, bottom: 20, left: 40},
	width = 960 - margin.left - margin.right,
	height = 500 - margin.top - margin.bottom;

var x = d3.scale.linear()
	.domain([0, n - 1])
	.range([0, width]);

var y = d3.scale.linear()
	.domain([-1, 1])
	.range([height, 0]);

var line = d3.svg.line()
	.interpolate("monotone")
	.x(function(d, i) { return x(i); })
	.y(function(d, i) { return y(d); });

var svg = d3.select("#graph").append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.append("defs").append("clipPath")
	.attr("id", "clip")
	.append("rect")
	.attr("width", width)
	.attr("height", height);

svg.append("g")
	.attr("class", "x axis")
	.attr("transform", "translate(0," + y(0) + ")")
	.call(d3.svg.axis().scale(x).orient("bottom"));

svg.append("g")
	.attr("class", "y axis")
	.call(d3.svg.axis().scale(y).orient("left"));

var path = svg.append("g")
	.attr("clip-path", "url(#clip)")
	.append("path")
	.datum(data)
	.attr("class", "line")
	.attr("d", line);

tick();

	</script>
</body>
</html>
