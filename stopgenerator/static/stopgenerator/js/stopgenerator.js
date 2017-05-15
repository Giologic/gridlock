var activeDialog;

$(document).ready(function () {
    console.log("stopgenerator.js: document is ready");

    $("#generate-stop-layout-btn").click(function () {
        console.log("stopgenerator.js: generate-stop-layout-btn clicked");
        var settings = stopLayoutDialogSettings[$('#stop-layout').val() - 1];
        showStopLayoutDialog(settings);
    });

    $("#clear-stops-btn").click(function () {
        console.log("stopgenerator.js: clear-stops-btn clicked");
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
    });
}