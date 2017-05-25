// Global variable where the location geometry layer instance will be stored
var locationBoundaryLayer;

// Global variable where the displayed stops layer will be stored
var stopsLayer;

// Global variable where the currently active Leaflet dialog will be displayed
var activeDialog;


$(document).ready(function () {
    console.log("demo.js: document is ready");

    initializeLocations();

    initializeStopsLayer();
    initializeStopLayouts();
    initializeStopManagement();


});

function initializeStopsLayer() {
    stopsLayer = L.featureGroup();
    stopsLayer.addTo(leafletMap);
}