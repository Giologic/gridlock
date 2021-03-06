// Global variable where the currently active Leaflet dialog will be displayed
var activeDialog;

$(document).ready(function () {
    console.log("demo.js: document is ready");

    initializeGtfsManagement();

    initializeLocations();

    initializeStopsLayer();
    initializeStopCount();
    initializeStopLayouts();
    initializeStopManagement();

    initializeRoutesLayer();
});

function showErrorDialog(errorMessage) {
    showDialog(errorDialogSettings, function () {
        $('#error-message-field').text(errorMessage);
    });
}

function showLoadingDialog(loadingMessage) {
    showDialog(loadingDialogSettings, function () {
         $('#loading-message-field').text(loadingMessage);
    });
}

function showDialog(settings, callback) {
    removeActiveDialog();
    activeDialog = L.control.dialog(settings["options"]).setContent(settings["content"]).addTo(leafletMap);
    activeDialog.layoutType = settings["name"];
    activeDialog.open();
    callback();
}

function showPermanentDialog(settings, callback) {
    var dialog  = L.control.dialog(settings["options"]).setContent(settings["content"]).addTo(leafletMap);
    dialog.open();
    callback();
}

function removeActiveDialog() {
    //noinspection EqualityComparisonWithCoercionJS
    if (activeDialog != null) {
        activeDialog.remove(leafletMap);
    }
}