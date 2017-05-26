$(document).ready(function() {
    console.log("stopremove.js: document is ready");
});

function enableStopDeletion() {
    enableAreaSelect(function(selectionEvent) {
        var selectedStopNodes = getSelectedStopNodes(selectionEvent);
        highlightStopNodes(selectedStopNodes);
    });
}

function disableStopDeletion() {
    disableAreaSelect();
    removeHighLightStopNodes(stopsLayer);
}