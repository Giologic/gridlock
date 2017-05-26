$(document).ready(function() {
    console.log("stopremove.js: document is ready");
});

function enableStopDeletion() {
    enableAreaSelect(function(selectionEvent) {
        var selectedStopNodes = getSelectedStopNodes(selectionEvent);
        highlightStopNodes(selectedStopNodes);
    });

    showDialog(removeStopDialogSettings, function() {
        $('#remove-stops-dialog-remove-selected-btn').click(function () {
            console.log("stopremove.js: remove-stops-dialog-remove-selected-btn clicked");

        });

        $('#remove-stops-dialog-remove-all-btn').click(function () {
            console.log("stopremove.js: remove-stops-dialog-remove-all-btn clicked");
            removeStopNodes(stopsLayer);
        });
    });
}

function removeStopNodes(stopNodes) {
    stopNodes.eachLayer(function (n) {
       stopsLayer.removeLayer(n);
    });
}

function disableStopDeletion() {
    disableAreaSelect();
    removeHighLightStopNodes(stopsLayer);
    removeActiveDialog();
}