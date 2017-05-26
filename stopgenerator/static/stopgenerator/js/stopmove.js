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

        if (!isSelectionEmpty(selectedStopNodes)) {
            // Zoom-in if necessary to fix unsolved lattice rotation bug
            if (numberOfStopNodes(selectedStopNodes) > 1) {
                leafletMap.fitBounds(selectedStopNodes.getBounds().pad(1 / 4));
            }
            addSelectedAreaPolygon(selectedStopNodes.getBounds(), selectedStopNodes);
        }
    });
}

function removeSelectedAreaPolygon() {
    selectionAreaPolygon.dragging.disable();
    selectionAreaPolygon.transform.disable();
    leafletMap.removeLayer(selectionAreaPolygon);
    selectionAreaPolygon = null;
}

function isSelectionEmpty(selectedStopNodes) {
    return Object.keys(selectedStopNodes.getBounds()).length <= 0;
}

function numberOfStopNodes(stopNodes) {
    return stopNodes.getLayers().length;
}

function addSelectedAreaPolygon(bounds, selectedStopNodes) {
    selectionAreaPolygon = createPolygonFromBounds(bounds);
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
    // if (selectionAreaPolygon != null) {
    //     removeSelectedAreaPolygon();
    // }
    disableAreaSelect();
    removeHighLightStopNodes(stopsLayer);
}