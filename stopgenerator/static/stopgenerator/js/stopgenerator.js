var stopsLayer; // Global variable where the displayed stops layer will be stored

var activeDialog; // TODO: Is this unnecessary?

$(document).ready(function () {
    console.log("stopgenerator.js: document is ready");
    initializeStopsLayer();

    $("#generate-stop-layout-form-button").click(function () {
        console.log("stopgenerator.js: generate-stop-layout-form-button clicked");
        var settings = stopLayoutDialogSettings[$('#stop-layout-selection').val() - 1];
        showStopLayoutDialog(settings);
    });

    $("#add-stops-button").click(function () {
        console.log("stopgenerator.js: add-stops-btn clicked");
    });

    $("#move-stops-button").click(function () {
        console.log("stopgenerator.js: move-stops-btn clicked");
    });

    $("#delete-stops-button").click(function () {
        console.log("stopgenerator.js: delete-stops-btn clicked");
    });
});

function initializeStopsLayer() {
    stopsLayer = L.featureGroup();
    stopsLayer.addTo(leafletMap);
}

function showStopLayoutDialog(settings, confirmCallback, cancelCallback) {
    //noinspection EqualityComparisonWithCoercionJS
    if (activeDialog != null) {
        activeDialog.remove(leafletMap);
    }
    activeDialog = L.control.dialog(settings["options"]).setContent(settings["content"]).addTo(leafletMap);
    activeDialog.open();


    $("#generate-stop-layout-dialog-button").click(function () {
        activeDialog.close();
        generateStops(function (stopLayoutNodes) {
            var selectedColor = $("#stops-color-field").val();
            displayStopNodes(stopLayoutNodes, selectedColor);
        });
    });
}

function generateStops(callback) {
    $.post(Urls['stopgenerator:generate_stop_layout'](), function (returnedData) {
        var stopLayoutNodes = returnedData['stop_layout_nodes'];
        console.log("stopgenerator.js:generateStops: response from server received");
        console.log(stopLayoutNodes);
        callback(stopLayoutNodes);
    });
}

function displayStopNodes(stopLayoutNodes, selectedColor) {
    var style = {
        radius: 5,
        fillColor: selectedColor,
        color: "#000000", // stop outline color
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };

    stopLayoutNodes.forEach(function(node) {
        var coord = node['coordinates'];
        var latLng = L.latLng(coord[1], coord[0]);
        var stopNodeMarker = L.circleMarker(latLng, style);
        stopsLayer.addLayer(stopNodeMarker);
    });
}