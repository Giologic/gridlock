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
          });
     });
  });
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