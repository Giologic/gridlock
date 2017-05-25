var selectionAreaPolygon;
var selectionAreaMultiPoints;

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

        var selectedStopNodes = getSelectedStopNodes(selectionEvent);

        if (Object.keys(selectedStopNodes.getBounds()).length > 0) { // If bounds is not empty
            leafletMap.fitBounds(selectedStopNodes.getBounds().pad(1 / 4));
            selectionAreaPolygon = createPolygonFromBounds(selectedStopNodes.getBounds());
            selectionAreaPolygon.addTo(leafletMap);
            selectionAreaPolygon.transform.enable({scaling: false});

            selectionAreaPolygon.on('rotate', function (rotation) {
                selectedStopNodes.eachLayer(function (stopNode) {
                   var matrix = rotation.layer.transform._matrix;
                   var transformedPoint = matrix.transform(stopNode._point);
                   stopNode.setLatLng(leafletMap.layerPointToLatLng(transformedPoint));
                });
            });

            selectionAreaPolygon.on('drag', function (event) {
                console.log(event);
            });
        }
    });
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

function createPolygonFromBounds(latLngBounds) {
    var northWest = latLngBounds.getNorthWest();
    var northEast = latLngBounds.getNorthEast();
    var southEast = latLngBounds.getSouthEast();
    var southWest = latLngBounds.getSouthWest();

    if (northEast.equals(southEast)) { // Horizontal line
        northEast = L.latLng(southEast.lat + 0.0001, southEast.lng + 0.0001);
        northWest = L.latLng(southWest.lat + 0.0001, southWest.lng + 0.0001);
    } else if (northWest.equals(northEast)) { // Vertical line
        northEast = L.latLng(northWest.lat + 0.0001, northWest.lng + 0.0001);
        southEast = L.latLng(southWest.lat + 0.0001, southWest.lng + 0.0001);
    }

    return new L.polygon([northWest, northEast, southEast, southWest], {draggable: true, transform: true});
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

function removeSelectedAreaPolygon() {
    selectionAreaPolygon.dragging.disable();
    selectionAreaPolygon.transform.disable();
    leafletMap.removeLayer(selectionAreaPolygon);
    selectionAreaPolygon = null;
}

function disableStopMovement() {
    //noinspection EqualityComparisonWithCoercionJS
    // if (selectionAreaPolygon != null) {
    //     removeSelectedAreaPolygon();
    // }
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

function disableAreaSelect() {
    leafletMap.off('areaselected');
    leafletMap.selectArea.disable();
    updateStopsHighlight(null);
    console.log("stopmanagement.js:disableAreaSelect: Area selection by dragging the mouse disabled");
}
