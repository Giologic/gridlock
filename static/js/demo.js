// Global variable where the currently active Leaflet dialog will be displayed
var activeDialog;

$(document).ready(function () {
    console.log("demo.js: document is ready");

    initializeLocations();

    initializeStopsLayer();
    initializeStopLayouts();
    initializeStopManagement();
});

