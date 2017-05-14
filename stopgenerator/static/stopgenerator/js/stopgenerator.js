$(document).ready(function () {
   console.log("stopgenerator.js: document is ready");

   $("#generate-stop-layout-btn").click(function () {
      console.log("stopgenerator.js: generate-stop-layout-btn clicked");
      generateStops(function () {
          
      });
   });

   $("#clear-stops-btn").click(function () {
       console.log("stopgenerator.js: clear-stops-btn clicked");
   })
});

function generateStops(callback) {
   $.post(Urls['stopgenerator:generate_stop_layout'](), function (returnedData) {
      console.log(returnedData['stop_layout_nodes']);
   });
}