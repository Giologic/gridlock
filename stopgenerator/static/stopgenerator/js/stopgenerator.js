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
    var dialog = L.control.dialog(settings["options"])
                  .setContent(settings["content"])
                  .addTo(leafletMap);
    dialog.open();
}

function generateStops(callback) {
    $.post(Urls['stopgenerator:generate_stop_layout'](), function (returnedData) {
        console.log(returnedData['stop_layout_nodes']);
    });
}