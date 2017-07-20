$(document).ready(function () {
    console.log("optimizer.js: document is ready");
    $('#networkoptimizer-optimize-route-network-btn').click(function () {
        var numEvolutions = $('#networkoptimizer-number-of-evolutions-field').val();
        var numMutationsPerEvolution = $('#networkoptimizer-number-mutations-per-evolutions-field').val();
        var numRemovals = $('#networkoptimizer-number-of-removals-field').val();
        var weightRandomFailure = $('#networkoptimizer-weight-random-failure-field').val();
        var weightTargetedFailure = $('#networkoptimizer-weight-targeted-failure-field').val();
        var weightRadiusOfGyration = $('#networkoptimizer-radius-of-gyration-field').val();
        var max_walking_dist = $('#routegen-maximum-walking-distance-field').val();
        optimizeRouteNetwork(numRemovals, weightRandomFailure,
            weightTargetedFailure, weightRadiusOfGyration, max_walking_dist,
            numEvolutions, numMutationsPerEvolution);
    });
});

function optimizeRouteNetwork(numRemovals, weightRandomFailure,
                              weightTargetedFailure, weightRadiusOfGyration,
                              max_walking_dist, numEvolutions, numMutationPerEvolution) {
    console.log('optimizer.js:optimizeRouteNetwork: route network optimization started');
    showLoadingDialog("The server is optimizing the route network, please wait a moment.");


    $.post(Urls['networkoptimizer:optimize_route_network'](), {
        'stop_node_coordinates': JSON.stringify(getCoordinatesOfDisplayedStops()),
        'route_network_coordinates': JSON.stringify(getRouteNetworkCoordinates()),
        'num_failure_removal': numRemovals,
        'weight_random_failure': weightRandomFailure,
        'weight_targeted_failure': weightTargetedFailure,
        'weight_radius_of_gyration': weightRadiusOfGyration,
        'max_walking_dist': max_walking_dist,
        'num_evolutions': numEvolutions,
        'num_mutations_per_evolution': numMutationPerEvolution
    }, function (returnedData) {
        clearRoutes();
        console.log("optimize.js:optimizeRouteNetwork: Response from server received");
        console.log(returnedData);
        var optimizedNetwork = JSON.parse(returnedData['optimized_network']);
        exportStrings = returnedData['export_string'];
        console.log(exportStrings);
        displayRouteNetwork(optimizedNetwork);
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


function getRouteNetworkCoordinates() {
    var routeNetworkCoordinates = [];
    routesLayer.eachLayer(function (route) {
       var routeCoordinates = [];
       route._latlngs.forEach(function (latlng) {
           routeCoordinates.push([latlng.lat, latlng.lng]);
       });
       routeNetworkCoordinates.push(routeCoordinates);
    });

    return routeNetworkCoordinates;
}

function snapStopsToRoad(map, roadFeatureGroup, stopsFeatureGroup) {
    stopsFeatureGroup.getLayers().forEach(function(layer) {
        var layerLatLng = layer.getLatLng();
        var snapped = L.GeometryUtil.closestLayerSnap(map, roadFeatureGroup.getLayers(), layerLatLng);
        layer.setLatLng(snapped.latlng);
    });
}