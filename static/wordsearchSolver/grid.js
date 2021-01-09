
//<input type="radio" name="display_{{wordEntry.index}}" data-index="{{wordEntry.index}}" value="mark" />
function radioClick() {
    if (this.checked) {
        wordIndex = this.dataset.index;
        letterPositions = wordLocations[wordIndex];
        if (letterPositions && letterPositions.length) {
            updateItem(letterPositions, wordIndex, this.value);
        }
    }
}

function updateItem(letterPositions, wordIndex, newType) {
    letterPositions.forEach(function (letterPosition) {
        gridHlEntry = gridHl[letterPosition];
        if (!gridHlEntry) {
            console.log("grid letter position doesn't exist!! " + letterPosition);
            return;
        }
        remOrAdd(gridHlEntry[0], wordIndex, newType === "highlight");
        remOrAdd(gridHlEntry[1], wordIndex, newType === "normal");
        recolour(letterPosition, gridHlEntry);
    });
}

function remOrAdd(arr, item, add) {
    index = arr.indexOf(item);
    if (add && index === -1) {
        arr.push(item);
        //console.log("Adding entry: " + item);
    }
    else if (!add && index > -1) {
        arr.splice(index, 1);
        //console.log("Removing entry: " + item);
    }
    else {
        //console.log("Ignoring entry " + item + ": " + add + " " + index);
    }
}

function setupRadio() {
    wordRadio = $("#wordList input");
    wordRadio.addClass("wordRadio");
    wordRadio.click(radioClick);
    wordRadio.each(function () {
        this.id = "radio" + this.dataset.index;
        this.name = "radio" + this.dataset.index;
        radioClick.call(this);
    });
}
function setupHover() {
    wordRows = $("#wordList tr");
    wordRows.each(function () {
        if (this.dataset.index) {
            this.id = "word" + this.dataset.index;
            $(this).hover(hlEntry, hlEntryClear);
        }
    });
    gridLetters = $("#grid td");
    gridLetters.hover(hlWords, hlWordsClear);
}

function recolour(letterPosition, gridHlEntry) {
    if (gridHlEntry[0].length) {
        applyClass(letterPosition, "Highlight");
    } else if (gridHlEntry[1].length) {
        applyClass(letterPosition, "Found");
    } else {
        applyClass(letterPosition, "None");
    }
}
function applyClass(element, newClass) {
    ele = $("#grid" + element);
    ele.removeClass("gridMatchHighlight gridMatchFound gridMatchNone").addClass("gridMatch" + newClass);
}

function hlEntry() {
    wordIndex = this.dataset.index;
    letterPositions = wordLocations[wordIndex];
    letterPositions.forEach(function (letterPosition) {
        $("#grid" + letterPosition).addClass("hover");
    });
    $(this).addClass("hover");
}
function hlEntryClear() {
    wordIndex = this.dataset.index;
    letterPositions = wordLocations[wordIndex];
    letterPositions.forEach(function (letterPosition) {
        $("#grid" + letterPosition).removeClass("hover");
    });
    $(this).removeClass("hover");
}
function hlWords() {
    gridIndex = this.dataset.index;
    $.each(wordLocations, function (index, locations) {
        if (locations.includes(gridIndex)) {
            $("#word" + index).addClass("hover");
        }
    });
    $(this).addClass("hover");
}
function hlWordsClear() {
    gridIndex = this.dataset.index;
    $.each(wordLocations, function (index, locations) {
        if (locations.includes(gridIndex)) {
            $("#word" + index).removeClass("hover");
        }
    });
    $(this).removeClass("hover");
}

$(document).ready(function () {
    setupRadio();
    setupHover();
})
