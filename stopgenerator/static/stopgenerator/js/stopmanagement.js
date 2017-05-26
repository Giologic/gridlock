var selectionAreaPolygon;

$(document).ready(function () {
    console.log("stopmanagement.js: document is ready");
});

function initializeStopManagement() {
    var addStopsButton = $("#add-stops-button");
    var moveStopsButton = $("#move-stops-button");
    var deleteStopsButton = $("#delete-stops-button");

    addStopsButton.click(function () {
        console.log('stopmanagement.js: add-stops-btn clicked');
        toggleButtonActive(addStopsButton, [moveStopsButton, deleteStopsButton]);
    });

    moveStopsButton.click(function () {
        console.log("stopmanagement.js: move-stops-btn clicked");
        toggleButtonActive(moveStopsButton, [addStopsButton, deleteStopsButton],
            enableStopMovement, disableStopMovement);
    });

    deleteStopsButton.click(function () {
        console.log("stopmanagement.js: delete-stops-btn clicked");
        toggleButtonActive(deleteStopsButton, [addStopsButton, moveStopsButton], enableStopDeletion, disableStopDeletion);
    });
}

/******** Button Management Utils ********/

function toggleButtonActive(buttonClicked, otherButtons, callbackActivate, callbackDeactivate) {
    if (buttonClicked.is(".pure-button-active")) {
        // Deactivate clicked button and enable other buttons
        buttonClicked.removeClass("pure-button-active");
        setDisabled(otherButtons, false);
        callbackDeactivate();
    } else {
        // Activate clicked button and disable other buttons
        buttonClicked.addClass("pure-button-active");
        setDisabled(otherButtons, true);
        callbackActivate();
    }
}

function setDisabled(buttons, disabled) {
    buttons.forEach(function(b) {
        b.attr('disabled', disabled);
    });
}

/*********** Selection Utils ************/
function enableAreaSelect(callback) {
    leafletMap.selectArea.enable();
    leafletMap.on('areaselected', function (selectionEvent) {
        callback(selectionEvent);
    });

    leafletMap.selectArea.setControlKey(false);
    console.log("stopmanagement.js:enableAreaSelect: Area selection by dragging the mouse enabled");
}


function disableAreaSelect() {
    leafletMap.off('areaselected');
    leafletMap.selectArea.disable();
    console.log("stopmanagement.js:disableAreaSelect: Area selection by dragging the mouse disabled");
}


function getSelectedStopNodes(selectionEvent) {
    var selectedStopNodes = L.featureGroup();
    stopsLayer.eachLayer(function (stopNode) {
        if (selectionEvent.bounds.contains(stopNode.getLatLng())) {
            selectedStopNodes.addLayer(stopNode);
        }
    });

    return selectedStopNodes;
}

function highlightStopNodes(stopNodes) {
    stopNodes.eachLayer(function(n) {
        setHighlight(n, true);
    });
}

function setHighlight(stopNode, highlighted) {
    stopNode.setStyle({
        color: highlighted ? 'red' : '#000000',
        weight: highlighted ? 2 : 1
    });
}

function removeHighLightStopNodes(stopNodes) {
        stopNodes.eachLayer(function(n) {
        setHighlight(n, false);
    });
}
