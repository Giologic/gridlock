$(document).ready(function () {
    console.log("stopmove.js: document is ready");
});

function enableStopMovement() {
    enableAreaSelect(function(selectionEvent) {
        //noinspection EqualityComparisonWithCoercionJS
        if (selectionAreaPolygon != null) {
            removeSelectedAreaPolygon();
        }

        var selectedStopNodes = getSelectedStopNodes(selectionEvent);
        highlightStopNodes(selectedStopNodes);
        addMovementControls(selectedStopNodes);
        disableAreaSelect();
    });

    showDialog(moveStopDialogSettings, function () {
        $('#move-stops-dialog-clear-selection-btn').click(function () {
            console.log("stopmove.js: move-stops-dialog-clear-selection-btn clicked");
            enableStopMovement();
            removeSelectedAreaPolygon();
            removeHighLightStopNodes(stopsLayer);
        });
    });
}

function removeSelectedAreaPolygon() {
    //noinspection EqualityComparisonWithCoercionJS
    if (selectionAreaPolygon != null) {
        selectionAreaPolygon.dragging.disable();
        selectionAreaPolygon.transform.disable();
        leafletMap.removeLayer(selectionAreaPolygon);
        selectionAreaPolygon = null;
    }
}

function addMovementControls(selectedStopNodes) {
    if (!isSelectionEmpty(selectedStopNodes)) {
        // Zoom-in if necessary to fix unsolved lattice rotation bug
        if (numberOfStopNodes(selectedStopNodes) > 1) {
            leafletMap.fitBounds(selectedStopNodes.getBounds().pad(0.25));
        }
        addSelectedAreaPolygon(selectedStopNodes.getBounds(), selectedStopNodes);
    }
}

function isSelectionEmpty(selectedStopNodes) {
    return Object.keys(selectedStopNodes.getBounds()).length <= 0;
}

function addSelectedAreaPolygon(bounds, selectedStopNodes) {
    selectionAreaPolygon = createPolygonFromBounds(bounds);
    selectionAreaPolygon.addTo(leafletMap);
    selectionAreaPolygon.transform.enable({scaling: false});

    selectionAreaPolygon.on('rotate', function (rotation) {
        transformStopNodes(selectedStopNodes, rotation.layer.transform._matrix);
    });

    selectionAreaPolygon.on('drag', function (event) {
        translateStopNodes(selectedStopNodes, event.movementX, event.movementY);
    });
}

function transformStopNodes(stopNodes, transformMatrix) {
    stopNodes.eachLayer(function (n) {
        var transformedPoint = transformMatrix.transform(n._point);
        n.setLatLng(leafletMap.layerPointToLatLng(transformedPoint));
    });
}

function translateStopNodes(stopNodes, xTranslate, yTranslate) {
    stopNodes.eachLayer(function (n) {
        var translatedPoint = L.point(n._point.x + xTranslate, n._point.y + yTranslate);
        n.setLatLng(leafletMap.layerPointToLatLng(translatedPoint));
    });
}

function createPolygonFromBounds(latLngBounds) {
    var northWest = latLngBounds.getNorthWest();
    var northEast = latLngBounds.getNorthEast();
    var southEast = latLngBounds.getSouthEast();
    var southWest = latLngBounds.getSouthWest();

    if (northEast.equals(southEast)) {
        // Stops are aligned horizontally
        northEast = L.latLng(southEast.lat + 0.0002, southEast.lng + 0.0002);
        northWest = L.latLng(southWest.lat + 0.0002, southWest.lng - 0.0002);
        southEast = L.latLng(southEast.lat - 0.0002, southEast.lng + 0.0002);
        southWest = L.latLng(southWest.lat - 0.0002, southWest.lng - 0.0002);
    } else if (northWest.equals(northEast)) {
        // Stops are aligned vertically
        northEast = L.latLng(northWest.lat + 0.0002, northWest.lng + 0.0002);
        southEast = L.latLng(southWest.lat - 0.0002, southWest.lng + 0.0002);
        northWest = L.latLng(northWest.lat + 0.0002, northWest.lng - 0.0002);
        southWest = L.latLng(southWest.lat - 0.0002, southWest.lng - 0.0002);
    }

    return new L.polygon([northWest, northEast, southEast, southWest], {draggable: true, transform: true});
}

function disableStopMovement() {
    //noinspection EqualityComparisonWithCoercionJS
    if (selectionAreaPolygon != null) {
        removeSelectedAreaPolygon();
    }
    disableAreaSelect();
    removeHighLightStopNodes(stopsLayer);
    removeActiveDialog();
}