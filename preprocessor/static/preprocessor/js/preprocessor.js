$(document).ready(function() {
    console.log("preprocessor.js: document is ready");

    var leafletMap = $('#leaflet-map');
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
       console.log(locationGeometry);
       // TODO: Implement displaying of location geometry
    });
}

function getLocationGeometry(locationPk, callback) {
     $.get(Urls['preprocessor:location_geometry'](), {'location_pk': locationPk}, function(returnedData) {
         callback(JSON.parse(returnedData['location_geometry']));
     });
}