$(document).ready(function () {
   console.log("stopadd.js: document is ready");
});

function enableStopAdding() {
    leafletMap.on('click', function(e){
        addStopNodeMarker(e.latlng, $("#add-stops-dialog-stop-color-field").val());
    });

    showDialog(addStopDialogSettings, function () {});
}

function disableStopAdding() {
    leafletMap.off('click');
    removeActiveDialog();
}

function addStopNodeMarker(latLng, selectedColor) {
    var style = {
        radius: 5,
        fillColor: selectedColor,
        color: "#000000", // stop outline color
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8,
    };

    var stopNodeMarker = L.circleMarker(latLng, style);
    stopsLayer.addLayer(stopNodeMarker);
}