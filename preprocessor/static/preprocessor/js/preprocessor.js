$(document).ready(function() {
    console.log("preprocessor.js: document is ready");
    displayLocationChoices($('#location-selection'));
});

function displayLocationChoices(locationSelection) {
    getLocations(function(locationList) {
        locationSelection.empty();
        locationList.forEach(function(location){
           addLocationAsOption(locationSelection, location);
        });
    });
}

function getLocations(callback) {
    $.get(Urls['preprocessor:location_list'](), function(returnedData) {
        callback(JSON.parse(returnedData['location_list']));
    });
}

function addLocationAsOption(locationSelection, location) {
    var locationPrimaryKey = location['pk'];
    var locationName = location['fields']['name'];
    locationSelection.append('<option value=' + locationPrimaryKey + '>' + locationName + '</option>');
}
