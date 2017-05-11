var LOCATION_LAYER_STYLE = {
    color: '#000000'
};

$(document).ready(function() {
    console.log("preprocessor.js: document is ready");

    var locationSelection = $('#location-selection');
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
        var locationLayer = L.geoJson(locationGeometry);
        locationLayer.setStyle(LOCATION_LAYER_STYLE);
        locationLayer.addTo(leafletMap);
        restrictToLayer(leafletMap, locationLayer);
    });
}

function restrictToLayer(leafletMap, layer) {
    leafletMap.fitBounds(layer.getBounds());
    leafletMap.setMaxBounds(layer.getBounds());
    leafletMap.options.minZoom = leafletMap.getZoom();

    console.log("preprocessor.js:restrictToLayer: Done");
}

function getLocationGeometry(locationPk, callback) {
    $.get(Urls['preprocessor:location_geometry'](), {'location_pk': locationPk}, function(returnedData) {
        callback(JSON.parse(returnedData['location_geometry']));
    });
}