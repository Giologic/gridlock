var LOCATION_GEOM_LAYER_STYLE = {
    color: '#000000'
};

// Global variable where the location geometry layer instance will be stored
var locationGeometryLayer;

$(document).ready(function() {
    console.log("preprocessor.js: document is ready");

    var locationSelection = $('#location-selection');
    locationSelection.change(function() {
        console.log("preprocessor.js: location selection changed");
        displayLocationGeometry(leafletMap, locationSelection.val());
    });

    displayLocationChoices(leafletMap, locationSelection);
});

function displayLocationChoices(leafletMap, locationSelection) {
    getLocations(function(locationList) {
        locationSelection.empty();
        locationList.forEach(function(location){
           addLocationAsOption(locationSelection, location);
        });
        displayLocationGeometry(leafletMap, locationSelection.val());
    });
}

function getLocations(callback) {
    $.get(Urls['preprocessor:location_list'](), function(returnedData) {
        callback(JSON.parse(returnedData['location_list']));
    });
}

function addLocationAsOption(locationSelection, location) {
    var locationPk = location['pk'];
    var locationName = location['fields']['name'];
    locationSelection.append('<option value=' + locationPk + '>' + locationName + '</option>');
}

function displayLocationGeometry(leafletMap, locationPk) {
    getLocationGeometry(locationPk, function(locationGeometry) {
        //noinspection EqualityComparisonWithCoercionJS
        if (locationGeometryLayer != null) {
            leafletMap.removeLayer(locationGeometryLayer);
        }

        locationGeometryLayer = L.geoJson(locationGeometry);
        locationGeometryLayer.setStyle(LOCATION_GEOM_LAYER_STYLE);
        locationGeometryLayer.addTo(leafletMap);
        restrictToLayer(leafletMap, locationGeometryLayer);
    });
}

function restrictToLayer(leafletMap, layer) {
    leafletMap.fitBounds(layer.getBounds());
    leafletMap.setMaxBounds(layer.getBounds());

    console.log("preprocessor.js:restrictToLayer: done");
}

function getLocationGeometry(locationPk, callback) {
    $.get(Urls['preprocessor:location_geometry'](), {'location_pk': locationPk}, function(returnedData) {
        callback(JSON.parse(returnedData['location_geometry']));
    });
}