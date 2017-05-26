// Global variable where the currently active Leaflet dialog will be displayed
var activeDialog;

$(document).ready(function () {
    console.log("demo.js: document is ready");

    initializeLocations();

    initializeStopsLayer();
    initializeStopLayouts();
    initializeStopManagement();
});

function showDialog(settings, callback) {
    //noinspection EqualityComparisonWithCoercionJS
    if (activeDialog != null) {
        activeDialog.remove(leafletMap);
    }

    activeDialog = L.control.dialog(settings["options"]).setContent(settings["content"]).addTo(leafletMap);
    activeDialog.layoutType = settings["name"];
    activeDialog.open();

    callback();
}
