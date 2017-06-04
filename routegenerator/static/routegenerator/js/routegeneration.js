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
        if (numberOfStopNodes(stopsLayer) > 1) {
            showLoadingDialog("The server is generating the routes, please wait a moment.");
            generateRouteNetwork();
        } else {
            showErrorDialog("There must be at least 2 stop nodes in order to generate routes." +
                " Please add more stop nodes.");
        }
    });

    $("#clear-routes-btn").click(function () {
       console.log("routegeneration.js: clear-routes-btn clicked");
       clearRoutes();
    });

    var showRoutesCheckbox = $("#show-generated-routes-checkbox");
    showRoutesCheckbox.change(function () {
        if (showRoutesCheckbox.is(':checked')) {
            console.log("routegeneration.js: show-generated-routes-checkbox checked");
            routesLayer.addTo(leafletMap);
        } else {
            console.log("routegeneration.js: show-generated-routes-checkbox unchecked");
            leafletMap.removeLayer(routesLayer);
        }
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
        removeActiveDialog();
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

function clearRoutes() {
    if (routesLayer !== null) {
        routesLayer.eachLayer(function (r) {
            routesLayer.removeLayer(r);
        });
    };
}