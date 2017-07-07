$(document).ready(function () {
    console.log("fitness.js: document is ready");
    $('#networkoptimizer-compute-fitness-score-btn').click(function () {
        var numRemovals = $('#networkoptimizer-number-of-removals-field').val();
        var weightRandomFailure = $('#networkoptimizer-weight-random-failure-field').val();
        var weightTargetedFailure = $('#networkoptimizer-weight-targeted-failure-field').val();
        var weightRadiusOfGyration = $('#networkoptimizer-radius-of-gyration-field').val();
        computeFitnessScore(numRemovals, weightRandomFailure, weightTargetedFailure, weightRadiusOfGyration);
    });
});

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

function computeFitnessScore(numRemovals, weightRandomFailure, weightTargetedFailure, weightRadiusOfGyration) {
    console.log('fitness.js:ComputeFitnessScore: computation of fitness score started');
    showLoadingDialog("The server is computing the fitness score, please wait a moment.");

    $.post(Urls['networkoptimizer:check_fitness_score'](), {
        'stop_node_coordinates': JSON.stringify(getCoordinatesOfDisplayedStops()),
        'route_network_coordinates': JSON.stringify(getRouteNetworkCoordinates()),
        'num_failure_removal': numRemovals,
        'weight_random_failure': weightRandomFailure,
        'weight_targeted_failure': weightTargetedFailure,
        'weight_radius_of_gyration': weightRadiusOfGyration
    }, function (returnedData) {
        console.log("fitness.js:checkFitnessScore: Response from server received");
        console.log(returnedData);
        removeActiveDialog();
    });
}