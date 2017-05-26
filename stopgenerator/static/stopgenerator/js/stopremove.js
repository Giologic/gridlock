$(document).ready(function() {
    console.log("stopremove.js: document is ready");
});

function enableStopDeletion() {
    var selectedStopNodes = null;
    enableAreaSelect(function(selectionEvent) {
        removeHighLightStopNodes(stopsLayer);
        selectedStopNodes = getSelectedStopNodes(selectionEvent);
        highlightStopNodes(selectedStopNodes);
    });

    showDialog(removeStopDialogSettings, function() {
        $('#remove-stops-dialog-remove-selected-btn').click(function () {
            console.log("stopremove.js: remove-stops-dialog-remove-selected-btn clicked");
            removeStopNodes(selectedStopNodes);
            updateStopCount();
        });

        $('#remove-stops-dialog-remove-all-btn').click(function () {
            console.log("stopremove.js: remove-stops-dialog-remove-all-btn clicked");
            removeStopNodes(stopsLayer);
            updateStopCount();
        });
    });
}

function removeStopNodes(stopNodes) {
    if (stopNodes !== null) {
        stopNodes.eachLayer(function (n) {
           stopsLayer.removeLayer(n);
        });
    }
}

function disableStopDeletion() {
    disableAreaSelect();
    removeHighLightStopNodes(stopsLayer);
    removeActiveDialog();
}