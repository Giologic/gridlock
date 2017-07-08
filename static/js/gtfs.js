$(document).ready(function () {
    console.log("gtfs.js: document is ready");
});

function initializeGtfsManagement() {
    $('#import-navbar-btn').click(function () {
        console.log("gtfs.js:initialiGtfsManagement: import-navbar-btn clicked");
        showDialog(importDialogSettings, function () {
            $('#start-import-btn').click(function () {
                console.log("gtfs.js:initializeGtfsManagement: import of existing state started");

                var configFileInput = document.getElementById("config-file-input");
                var reader = new FileReader();
                reader.onload = function (e) {
                    var inputLines = reader.result.split("\n");
                    inputLines.forEach(loadInput);
                };

                reader.readAsText(configFileInput.files[0]);
            });
        });
    });

    $('#export-navbar-btn').click(function () {
        console.log("gtfs.js:initialGtfsManagement: export-navbar-btn clicked");
        showDialog(exportDialogSettings, function() {
            $('#start-export-btn').click(function () {
                console.log("gtfs.js:initializeGtfsManagement: export of current state started");
                var gtfsData = [];
                if ($('#export-stops-checkbox').is(':checked')) {
                    Array.prototype.push.apply(gtfsData, getStopsGtfs());
                }
                if ($('#export-routes-checkbox').is(':checked')) {
                    Array.prototype.push.apply(gtfsData, getRoutesGtfs());
                }

                var blob = new Blob(gtfsData, {type: "text/plain;charset=utf-8"});
                saveAs(blob, $('#export-filename-field').val());
                removeActiveDialog();
            });
        });
    });

    $('#graph-export-navbar-btn').click(function () {
        console.log(exportStrings);
        var blob = new Blob([exportStrings], {type: "text/plain;charset=utf-8"});
        saveAs(blob, "exported_graph_data.txt");
    });
}

function loadInput(inputStr) {
    if (inputStr.match('stop, .*')) {
        loadStopGtfs(inputStr);
    } else if (inputStr.match('route, .*')) {
        loadRouteGtfs(inputStr);
    } else {
        console.log("gtfs.js:loadinput: invalid input string read");
    }
}

function loadStopGtfs(inputStr) {
    console.log("gtfs.js:loadStopGtfs: stop has been loaded");
    var data = inputStr.split(', ');
    var lat = parseFloat(data[1]);
    var lng = parseFloat(data[2]);
    var color = data[3];
    addStopNodeMarker(L.latLng(lat, lng), color);
}

function loadRouteGtfs(inputStr) {
    console.log("gtfs.js:loadRouteGtfs: route has been loaded");
    var data = inputStr.split(', ');
    var routePoints = JSON.parse(data[1]);
    var polyLine = L.polyline(routePoints);
    routesLayer.addLayer(polyLine);
}

function getStopsGtfs() {
    var stopsData = [];
    stopsLayer.getLayers().forEach(function (s) {
        stopsData.push("stop" + ", " + s._latlng.lat + ", "  + s._latlng.lng + ", " + s.options['fillColor'] + "\n");
    });
    return stopsData;
}

function getRoutesGtfs() {
    var routesData = [];
    routesLayer.getLayers().forEach(function (r) {
        routesData.push("route" + ", " +  JSON.stringify(convertToLatlngTuple(r.getLatLngs())) + "\n");
    });
    return  routesData;
}

function convertToLatlngTuple(latLngs) {
    var ret = [];
    latLngs.forEach(function (l) {
        ret.push([l.lat, l.lng]);
    });
    return ret;
}