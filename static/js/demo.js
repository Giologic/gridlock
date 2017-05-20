var locationBoundaryLayer; // Global variable where the location geometry layer instance will be stored
var stopsLayer; // Global variable where the displayed stops layer will be stored

var activeDialog;

$(document).ready(function () {
    console.log("demo.js: document is ready");

    /******* PREPROCESSOR UI SETUP *******/
    var locationSelection = $('#location-selection');
    locationSelection.change(function () {
        console.log("demo.js: location selection changed");
        displayLocationGeometry(leafletMap, locationSelection.val());
    });

    displayLocationChoices(leafletMap, locationSelection);

    /******* STOP GENERATOR UI SETUP *******/
    initializeStopsLayer();

    $("#generate-stop-layout-form-button").click(function () {
        console.log("demo.js: generate-stop-layout-form-button clicked");
        var settings = stopLayoutDialogSettings[$('#stop-layout-selection').val() - 1];
        showStopLayoutDialog(settings);
    });

    $("#add-stops-button").click(function () {
        console.log("demo.js: add-stops-btn clicked");
    });

    $("#move-stops-button").click(function () {
        console.log("demo.js: move-stops-btn clicked");
        // TODO: Leaflet.Path.Transform (https://github.com/w8r/Leaflet.Path.Transform) to rotate and translate stops
    });

    $("#delete-stops-button").click(function () {
        console.log("demo.js: delete-stops-btn clicked");
        // TODO: leaflet-area-select (https://github.com/w8r/leaflet-area-select) to select stops
    });
});
