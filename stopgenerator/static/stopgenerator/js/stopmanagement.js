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
        toggleButtonActive(deleteStopsButton, [addStopsButton, moveStopsButton], enableStopDeletion, disableAreaSelect);
    });
}

function enableStopDeletion() {
    enableAreaSelect(function(selectionEvent) {
        updateStopsHighlight(selectionEvent);
    });
}

function enableStopMovement() {
    enableAreaSelect(function(selectionEvent) {
        //noinspection EqualityComparisonWithCoercionJS
        if (selectionAreaPolygon != null) {
            removeSelectedAreaPolygon();
        }

        selectionAreaPolygon = createPolygonFromBounds(selectionEvent.bounds);
        selectionAreaPolygon.addTo(leafletMap);
        selectionAreaPolygon.transform.enable({scaling: false});
    });
}

function removeSelectedAreaPolygon() {
    selectionAreaPolygon.dragging.disable();
    selectionAreaPolygon.transform.disable();
    leafletMap.removeLayer(selectionAreaPolygon);
    selectionAreaPolygon = null;
}

function disableStopMovement() {
    //noinspection EqualityComparisonWithCoercionJS
    if (selectionAreaPolygon != null) {
        removeSelectedAreaPolygon();
    }
    disableAreaSelect();
}

function toggleButtonActive(buttonClicked, otherButtons, callbackActivate, callbackDeactivate) {
    if (buttonClicked.is(".pure-button-active")) {
        // Deactivate clicked button
        buttonClicked.removeClass("pure-button-active");
        setDisabled(otherButtons, false);
        callbackDeactivate();
    } else {
        // Activate clicked button
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

function enableAreaSelect(callback) {
    leafletMap.selectArea.enable();
    leafletMap.on('areaselected', function (selectionEvent) {
        callback(selectionEvent);
    });

    leafletMap.selectArea.setControlKey(false);
    console.log("stopmanagement.js:enableAreaSelect: Area selection by dragging the mouse enabled");
}


function createPolygonFromBounds(latLngBounds) {
  var polygon =  new L.polygon([latLngBounds.getNorthWest(), latLngBounds.getNorthEast(),
      latLngBounds.getSouthEast(), latLngBounds.getSouthWest()], {draggable: true, transform: true});
  return polygon;
}

function updateStopsHighlight(selectionEvent) {
    if (selectionEvent === null) {
        // Remove highlighting of all stop nodes
        stopsLayer.eachLayer(function (stopNode) {
            setHighlight(stopNode, false);
        });
    } else {
        // Highlight nodes that are inside the selection bounds
        L.Util.requestAnimFrame(function () {
            stopsLayer.eachLayer(function (stopNode) {
                setHighlight(stopNode, selectionEvent.bounds.contains(stopNode.getLatLng()));
            }) ;
        });
    }
}

function setHighlight(stopNode, highlighted) {
    stopNode.setStyle({
        color: highlighted ? 'red' : '#000000',
        weight: highlighted ? 2 : 1
    });
}

function disableAreaSelect() {
    leafletMap.off('areaselected');
    leafletMap.selectArea.disable();
    updateStopsHighlight(null);
    console.log("stopmanagement.js:disableAreaSelect: Area selection by dragging the mouse disabled");
}
