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
        toggleButtonActive(moveStopsButton, [addStopsButton, deleteStopsButton], enableAreaSelect, disableAreaSelect);
    });

    deleteStopsButton.click(function () {
        console.log("stopmanagement.js: delete-stops-btn clicked");
        toggleButtonActive(deleteStopsButton, [addStopsButton, moveStopsButton], enableAreaSelect, disableAreaSelect);
    });
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

function enableAreaSelect() {
    leafletMap.selectArea.enable();
    leafletMap.on('areaselected', function (e) {
        console.log(e.bounds.toBBoxString()); // lon, lat, lon, lat
    });
    leafletMap.selectArea.setControlKey(false);
    console.log("stopmanagement.js:enableAreaSelect: Area selection via CTRL key enabled");
}

function disableAreaSelect() {
    leafletMap.selectArea.disable();
    console.log("stopmanagement.js:disableAreaSelect: Area selection via CTRL key disabled");
}

