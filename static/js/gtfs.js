$(document).ready(function () {
    console.log("gtfs.js: document is ready");
});

function initializeGtfsManagement() {
  $('#import-navbar-btn').click(function () {
      console.log("gtfs.js:initialiGtfsManagement: import-navbar-btn clicked");
      showDialog(importDialogSettings, function () {

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