var activeDialog;

$(document).ready(function () {
    console.log("stopgenerator.js: document is ready");

    $("#generate-stop-layout-button").click(function () {
        console.log("stopgenerator.js: generate-stop-layout-btn clicked");
        var settings = stopLayoutDialogSettings[$('#stop-layout-selection').val() - 1];
        showStopLayoutDialog(settings);
    });

    $("#clear-stops-button").click(function () {
        console.log("stopgenerator.js: clear-stops-btn cˆlicked");
    });
});

function showStopLayoutDialog(settings, confirmCallback, cancelCallback) {
    //noinspection EqualityComparisonWithCoercionJS
    if (activeDialog != null) {
        activeDialog.remove(leafletMap);
    }

    activeDialog = L.control.dialog(settings["options"]).setContent(settings["content"]).addTo(leafletMap);
    activeDialog.open();
}

function generateStops(callback) {
    $.post(Urls['stopgenerator:generate_stop_layout'](), function (returnedData) {
        console.log(returnedData['stop_layout_nodes']);
        displayStopNodes(returnedData['stop_layout_nodes']);
    });
}

function displayStopNodes(stopNodes) {
    var stopsLayer = L.featureGroup();
    stopsLayer.addTo(leafletMap);

    stopNodes.forEach(function(node) {
        var coord = node['coordinates'];
        var latLng = L.latLng(coord[1], coord[0]);
        var stopNodeMarker = L.circleMarker(latLng, STOP_NODE_STYLE);
        stopsLayer.addLayer(stopNodeMarker);

    });
}