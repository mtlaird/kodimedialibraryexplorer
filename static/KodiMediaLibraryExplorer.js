function SearchListItems(SearchTerm) {
    const listItems = document.getElementsByTagName("li");
    SearchTerm = SearchTerm.toLowerCase();
    for (let i=0; i < listItems.length; i++) {
        listItems[i].hidden = listItems[i].innerText.toLowerCase().search(SearchTerm) === -1;
    }
}


function RegisterSearchField(FieldID) {
    let SearchField = document.getElementById(FieldID);
    if (SearchField != null) {
        SearchField.setAttribute("oninput", "SearchListItems(this.value)");
    }
}


function ClearSearchField(FieldID) {
    let SearchField = document.getElementById(FieldID);
    if (SearchField != null) {
        SearchField.value = "";
        SearchListItems("");
    }
}

function RegisterClearButton(ButtonID, FieldID) {
    let ClearButton = document.getElementById(ButtonID);
    if (ClearButton != null) {
        ClearButton.setAttribute("onclick", "ClearSearchField(\"" + FieldID + "\")");
    }
}