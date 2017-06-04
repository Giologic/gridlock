// Global variable where the displayed routes layer will be stored
var routesLayer;

$(document).ready(function () {
   console.log("routegeneration.js: document is ready");
});

function initializeRoutesLayer() {
    routesLayer = L.featureGroup();
    routesLayer.addTo(leafletMap);

    $("#generate-routes-btn").click(function () {
        console.log("routegeneration.js: generate-routes-btn clicked");
        generateRouteNetwork();
    });
}

function generateRouteNetwork() {
    var parameters = {
        'stop_node_coordinates': JSON.stringify(getCoordinatesOfDisplayedStops()),
        'maximum_walking_distance': $("#routegen-maximum-walking-distance-field").val(),
        'number_of_generations': $("#routegen-number-of-generations-field").val()
    };

    console.log("routegeneration.js:generateRouteNetwork: generation of routes started");
    $.post(Urls['routegenerator:generate_route_network'](), parameters, function (returnedData) {
        var routeNetwork = JSON.parse(returnedData['route_network']);
        console.log("routegeneration.js:generateRouteNetwork: response from server received");
        console.log(routeNetwork);
        displayRouteNetwork(routeNetwork);
        snapStopsToRoad(leafletMap, routesLayer, stopsLayer);
    });
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

function snapStopsToRoad(map, roadFeatureGroup, stopsFeatureGroup) {
    stopsFeatureGroup.getLayers().forEach(function(layer) {
        var layerLatLng = layer.getLatLng();
        var snapped = L.GeometryUtil.closestLayerSnap(map, roadFeatureGroup.getLayers(), layerLatLng);
        layer.setLatLng(snapped.latlng);
    });
}