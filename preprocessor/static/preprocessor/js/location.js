$(document).ready(function () {
    console.log("location.js: document is ready");
});

function displayLocationChoices(leafletMap, locationSelection) {
    getLocations(function (locationList) {
        locationSelection.empty();
        locationList.forEach(function (location){
           addLocationAsOption(locationSelection, location);
        });
        displayLocationGeometry(leafletMap, locationSelection.val());
        console.log("location.js:displayLocationChoices: location choices display in select");
    });
}

function getLocations(callback) {
    $.get(Urls['preprocessor:location_list'](), function (returnedData) {
        callback(JSON.parse(returnedData['location_list']));
    });
}

function addLocationAsOption(locationSelection, location) {
    var locationPk = location['pk'];
    var locationName = location['fields']['name'];
    locationSelection.append('<option value=' + locationPk + '>' + locationName + '</option>');
}

function displayLocationGeometry(leafletMap, locationPk) {
    getLocationGeometry(locationPk, function (locationGeometry) {
        //noinspection EqualityComparisonWithCoercionJS
        if (locationBoundaryLayer != null) {
            leafletMap.removeLayer(locationBoundaryLayer);
        }

        locationBoundaryLayer = L.geoJson(locationGeometry);
        var style = {
          color: '#000000'
        };
        locationBoundaryLayer.setStyle(style);
        locationBoundaryLayer.addTo(leafletMap);

        console.log("location.js:displayLocationGeometry: location geometry displayed on map");
        restrictToLayer(leafletMap, locationBoundaryLayer);
    });
}

function getLocationGeometry(locationPk, callback) {
    $.get(Urls['preprocessor:location_geometry'](), {'location_pk': locationPk}, function (returnedData) {
        callback(JSON.parse(returnedData['location_geometry']));
    });
}

function restrictToLayer(leafletMap, layer) {
    leafletMap.fitBounds(layer.getBounds());
    leafletMap.setMaxBounds(layer.getBounds());
    console.log("location.js:restrictToLayer: map display restricted to layer");
}

function getLocationCenterLatLng() {
    var locationBounds = locationBoundaryLayer.getBounds();
    var locationCenter = locationBounds.getCenter();
    console.log("stoplayout.js:getLocationCenterLatLng: location center LatLng calculated as ("
        + locationCenter.lat + ", " + locationCenter.lng + ")");
    return locationCenter;
}

function getRecommendedPredefinedMeans(locationPk, callback) {
    $.get(Urls['preprocessor:location_recommended_predefined_means'](),
        {'location_pk': locationPk}, function (returnedData) {
        callback(returnedData['location_recommended_predefined_means'])
    })
}
