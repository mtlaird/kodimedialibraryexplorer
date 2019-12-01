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


function BuildArrayFromTableContents(TableID) {
    let Table = document.getElementById(TableID);
    let TableArray = [];
    let TableRow, RowArray;
    for (let i=0;  i < Table.getElementsByTagName('tr').length; i++) {
        TableRow = Table.getElementsByTagName('tr')[i];
        if (TableRow.getElementsByTagName('th').length === 0) {
            RowArray = [];
            for (let j=0; j < TableRow.getElementsByTagName('td').length; j ++) {
                RowArray.push(TableRow.getElementsByTagName('td')[j].innerHTML);
            }
            TableArray.push(RowArray);
        }
    }
    return TableArray;
}

function ReplaceTableContentsWithArray(TableID, TableArray) {
    let Table = document.getElementById(TableID);
    let TableRow;
    for (let i=Table.getElementsByTagName('tr').length-1; i>=0; i--) {
        TableRow = Table.getElementsByTagName('tr')[i];
        if (TableRow.getElementsByTagName('td').length > 0) {
            Table.deleteRow(i);
        }
    }
    for (let i=1; i<TableArray.length+1; i++) {
        Table.insertRow(i);
        for (let j=0; j<TableArray[i-1].length; j++) {
            Table.rows[i].insertCell(j);
            Table.rows[i].cells[j].innerHTML = TableArray[i-1][j];
        }
    }
}

function SortTableArray(TableArray, SortType, SortIndex, SortStatus) {
    let EndSortStatus;
    if (SortStatus === "Unsorted" || SortStatus === "Ascending") { EndSortStatus = "Descending"; }
    else { EndSortStatus = "Ascending"; }
    switch (SortType) {
        case "Numeric":
            return TableArray.sort(function (a, b) {
                if (EndSortStatus === "Ascending") { return a[SortIndex] - b[SortIndex]; }
                else { return b[SortIndex] - a[SortIndex]; }
            });
        case "String":
            return TableArray.sort(function (a, b) {
                if (EndSortStatus === "Ascending") { return b[SortIndex].localeCompare(a[SortIndex]); }
                else { return a[SortIndex].localeCompare(b[SortIndex]); }
            });
        case "HTML":
            return TableArray.sort(function (a, b) {
                let a_value, b_value;
                if (a[SortIndex].indexOf('<a href') !== -1) {
                    let span = document.createElement('span');
                    span.innerHTML = a[SortIndex];
                    a_value = span.textContent || span.innerText;
                }
                else { a_value = a[SortIndex]; }
                if (b[SortIndex].indexOf('<a href') !== -1) {
                    let span = document.createElement('span');
                    span.innerHTML = b[SortIndex];
                    b_value = span.textContent || span.innerText;
                }
                else { b_value = b[SortIndex]; }
                if (EndSortStatus === "Ascending") { return b_value.localeCompare(a_value); }
                else { return a_value.localeCompare(b_value); }
            });
        }
}

function ClearTableSortStatus(TableID) {
    let TableHeaderRow = document.getElementById(TableID).getElementsByTagName('tr')[0];
    let TableHeaderLen = TableHeaderRow.getElementsByTagName('th').length;
    for (let i=0; i < TableHeaderLen; i ++) {
        document.getElementById(TableID + i + "-sort-status").innerHTML = "";
    }
}

/**
 * @return {string}
 */
function GetSortStatus(TableID, SortIndex) {
    let SortStatus = document.getElementById(TableID + SortIndex + "-sort-status").innerHTML.charCodeAt(0);
    if (SortStatus === 9663) { return "Descending"; }
    if (SortStatus === 9653) { return "Ascending"; }
    return "Unsorted";
}

function SortTable(TableID, SortType, SortIndex) {
    let TableArray = BuildArrayFromTableContents(TableID);
    let StartSortStatus = GetSortStatus(TableID, SortIndex);
    let SortedTableArray = SortTableArray(TableArray, SortType, SortIndex, StartSortStatus);
    ReplaceTableContentsWithArray(TableID, SortedTableArray);
    ClearTableSortStatus(TableID);
    if (StartSortStatus === "Unsorted" || StartSortStatus === "Ascending") {
        document.getElementById(TableID + SortIndex + "-sort-status").innerHTML = String.fromCharCode(9663);
    }
    else {
        document.getElementById(TableID + SortIndex + "-sort-status").innerHTML = String.fromCharCode(9653);
    }
}

function RegisterTableHeader(TableID) {
    let Table = document.getElementById(TableID);
    if (Table != null) {
        let TableHeaderRow = Table.getElementsByTagName('tr')[0];
        let TableHeaderCell;
        for (let i=0; i < TableHeaderRow.getElementsByTagName('th').length; i++) {
            TableHeaderCell = TableHeaderRow.getElementsByTagName('th')[i];
            let span = document.createElement("span");
            span.setAttribute("id", TableID + i + "-sort-status");
            TableHeaderCell.appendChild(span);
            if (TableHeaderCell.innerText === "Title") {
                TableHeaderCell.setAttribute("onclick", "SortTable(\"" + TableID + "\", \"HTML\", " + i +")");
            }
            else if (TableHeaderCell.innerText === "Avg" || TableHeaderCell.innerText === "Pop" || TableHeaderCell.innerText === "Year") {
                TableHeaderCell.setAttribute("onclick", "SortTable(\"" + TableID + "\", \"Numeric\", " + i +")");
            }
            else {
                TableHeaderCell.setAttribute("onclick", "SortTable(\"" + TableID + "\", \"String\", " + i +")");
            }
        }
    }
}