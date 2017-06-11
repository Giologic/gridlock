$(document).ready(function () {
    console.log("gtfs.js: document is ready");
});

function initializeGtfsManagement() {
  $('#import-navbar-btn').click(function () {
      console.log("gtfs.js:initialiGtfsManagement: import-navbar-btn clicked");
      showDialog(importDialogSettings, function () {
          $('#start-import-btn').click(function () {
              console.log("gtfs.js:initializeGtfsManagement: import of existing state started");
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

function readSingleFile(e) {
  var file = e.target.files[0];
  if (!file) {
    return;
  }

  var reader = new FileReader();
  reader.onload = function(e) {
    var contents = e.target.result;
    displayContents(contents);
  };

  reader.readAsText(file);
}