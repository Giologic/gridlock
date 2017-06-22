// Global variable where the displayed stops layer will be stored
var stopsLayer;

$(document).ready(function () {
    console.log("stoplayout.js: document is ready");
});

function initializeStopsLayer() {
    stopsLayer = L.featureGroup();
    stopsLayer.addTo(leafletMap);
}

function initializeStopLayouts() {
    $("#generate-stop-layout-form-button").click(function () {
        console.log("stoplayout.js: generate-stop-layout-form-button clicked");
        var settings = stopLayoutDialogSettings[$('#stop-layout-selection').val() - 1];
        showStopLayoutDialog(settings);
    });
}

function showStopLayoutDialog(settings) {
    showDialog(settings, function () {
        setupDialogGenerateButton();
        setupDialogCheckboxes();
    });
}

function setupDialogGenerateButton() {
    $("#generate-stop-layout-dialog-button").click(function () {
        activeDialog.close();

        var layoutConfig = {};
        if (activeDialog.layoutType === "LATTICE") {
            setupLatticeLayoutConfig(layoutConfig);
        } else if (activeDialog.layoutType === "RANDOM") {
            setupRandomLayoutConfig(layoutConfig);
        } else if (activeDialog.layoutType === "N-BLOB") {
            setupNBlobLayoutConfig(layoutConfig);
        } else {
           throw "Active dialog has an invalid layoutdialogs type.";
        }
    });
}

function setupLatticeLayoutConfig(layoutConfig) {
    setupLayoutBaseConfig(layoutConfig);
    layoutConfig.layout_type = "LATTICE";

    if ($('#loc-center-lattice-start-checkbox').is(':checked')) {
        var locationCenterLatLng = getLocationCenterLatLng();
        layoutConfig.lattice_start_lat = locationCenterLatLng.lat;
        layoutConfig.lattice_start_lng = locationCenterLatLng.lng;
    } else {
        layoutConfig.lattice_start_lat = $('#lattice-start-lat-field').val();
        layoutConfig.lattice_start_lng = $('#lattice-start-lng-field').val();
    }

    generateStops(layoutConfig, displayStopNodes);
    console.log("stoplayout.js:setupLatticeLayoutConfig: generation of lattice layoutdialogs started");
}

function setupLayoutBaseConfig(layoutConfig) {
    layoutConfig.max_num_stops = $("#max-num-stops-field").val();
    layoutConfig.max_walking_dist = $("#max-walking-dist-field").val();
    layoutConfig.color = $("#stops-color-field").val();
}

function generateStops(layoutConfig, callback) {
    $.post(Urls['stopgenerator:generate_stop_layout'](), layoutConfig, function (returnedData) {
        var stopLayoutNodes = returnedData['stop_layout_nodes'];
        console.log("stoplayout.js:generateStops: response from server received");
        console.log(stopLayoutNodes);
        callback(stopLayoutNodes, layoutConfig.color);
    });
}

function displayStopNodes(stopLayoutNodes, selectedColor) {
    stopLayoutNodes.forEach(function(node) {
        var coord = node['latlng'];
        var latLng = L.latLng(coord[0], coord[1]);
        addStopNodeMarker(latLng, selectedColor);
    });
    updateStopCount();
}

function setupRandomLayoutConfig(layoutConfig) {
    setupLayoutBaseConfig(layoutConfig);
    layoutConfig.layout_type = "RANDOM";
    layoutConfig.location_pk = $('#location-selection').val();
    generateStops(layoutConfig, displayStopNodes);
    console.log("stoplayout.js:setupRandomLayoutConfig: generation of random layoutdialogs started");
}

function setupNBlobLayoutConfig(layoutConfig) {
    setupLayoutBaseConfig(layoutConfig);
    layoutConfig.layout_type = "N-BLOB";

    if ($('#recommended-predefined-means-checkbox').is(':checked')) {
        getRecommendedPredefinedMeans($('#location-selection').val(),
            function(loc_recommended_predefined_means_json) {
                layoutConfig.predefined_means = loc_recommended_predefined_means_json;
                generateStops(layoutConfig, displayStopNodes);
                console.log("stoplayout.js:setupNBlobLayoutConfig: generation of n-blob layoutdialogs " +
                    "using recommended predefined means started");
            }
        );
    } else {
        layoutConfig.predefined_means = '[' + $('#predefined-means-field').val() + ']';
        generateStops(layoutConfig, displayStopNodes);
        console.log("stoplayout.js:setupNBlobLayoutConfig: generation of n-blob layoutdialogs " +
                    "using manually entered predefined means started");
    }
}

function setupDialogCheckboxes() {
    if (activeDialog.layoutType === "LATTICE") {
        var locCenterLatticeStartCheckbox = $('#loc-center-lattice-start-checkbox');
        locCenterLatticeStartCheckbox.change(function () {
            $('#lattice-start-lat-field').attr('disabled', locCenterLatticeStartCheckbox.is(':checked'));
            $('#lattice-start-lng-field').attr('disabled', locCenterLatticeStartCheckbox.is(':checked'));
        });
    } else if (activeDialog.layoutType === "N-BLOB") {
        var recommendedPredefinedMeansCheckbox = $('#recommended-predefined-means-checkbox');
        recommendedPredefinedMeansCheckbox.change(function() {
            $('#predefined-means-field').attr('disabled', recommendedPredefinedMeansCheckbox.is(':checked'));
        });
    }
}