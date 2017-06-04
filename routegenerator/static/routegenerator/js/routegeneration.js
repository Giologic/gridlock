// Global variable where the displayed routes layer will be stored
var routesLayer;

$(document).ready(function () {
   console.log("routegeneration.js: document is ready");

   $("#generate-routes-btn").click(function () {
      console.log("routegeneration.js: generate-routes-btn clicked");
      var stopCoordinates = JSON.stringify(getCoordinatesOfDisplayedStops());
      $.post(Urls['routegenerator:generate_route_network'](), {'stop_node_coordinates': stopCoordinates}, function (returnedData) {
          var routeNetwork = JSON.parse(returnedData['route_network']);
          console.log(routeNetwork);
          displayRouteNetwork(routeNetwork);
      });
   });
});

function generateRouteNetwork(numGenerations) {
    for (var i = 0; i < numGenerations; i++) {
        generateRoute();
    }
}

function generateRoute() {
    var data = {};
    $.post(Urls['routegenerator:generate_route'](), data, function (returnedData) {
        createPolyline(JSON.parse(returnedData['route']));
    });
}

function initializeRoutesLayer() {
    routesLayer = L.featureGroup();
    routesLayer.addTo(leafletMap);
}

function getCoordinatesOfDisplayedStops() {
    var stopCoordinates = [];
    stopsLayer.getLayers().forEach(function (stopNode) {
        var latLng = stopNode._latlng;
        stopCoordinates.push([latLng.lat, latLng.lng]);
    });

    return stopCoordinates;
}

function displayRouteNetwork(routeNetwork) {
    console.log(routeNetwork);
    routeNetwork.forEach(function(route) {
        routesLayer.addLayer(createPolyline(route));
    });
}

function createPolyline(route) {
    var stopNodesLatLngs = [];
    route.forEach(function (stopNode) {
       stopNodesLatLngs.push(stopNode.attributes.latlng);
    });

    return L.polyline(stopNodesLatLngs);
}