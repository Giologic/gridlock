$(document).ready(function () {
    console.log("fitness.js: document is ready");
    $('#networkoptimizer-optimize-route-network-btn').click(function () {
        var numRemovals = $('#networkoptimizer-number-of-removals-field').val();
        var weightRandomFailure = $('#networkoptimizer-weight-random-failure-field').val();
        var weightTargetedFailure = $('#networkoptimizer-weight-targeted-failure-field').val();
        var weightRadiusOfGyration = $('#networkoptimizer-radius-of-gyration-field').val();
        computeFitnessScore(numRemovals, weightRandomFailure, weightTargetedFailure, weightRadiusOfGyration);
    });
});

function optimizeRouteNetwork() {

}