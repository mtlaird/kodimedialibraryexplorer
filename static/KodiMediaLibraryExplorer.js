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

function SortTableArray(TableArray, SortType, SortIndex) {
    switch (SortType) {
        case "Numeric":
            return TableArray.sort(function (a, b) {
                return b[SortIndex] - a[SortIndex];
            });
        case "String":
            return TableArray.sort(function (a, b) {
                return a[SortIndex].localeCompare(b[SortIndex]);
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
                return a_value.localeCompare(b_value);
            });
        }
}

function SortTable(TableID, SortType, SortIndex) {
    let TableArray = BuildArrayFromTableContents(TableID);
    let SortedTableArray = SortTableArray(TableArray, SortType, SortIndex);
    ReplaceTableContentsWithArray(TableID, SortedTableArray);
}

function RegisterTableHeader(TableID) {
    let Table = document.getElementById(TableID);
    if (Table != null) {
        let TableHeaderRow = Table.getElementsByTagName('tr')[0];
        let TableHeaderCell;
        for (let i=0; i < TableHeaderRow.getElementsByTagName('th').length; i++) {
            TableHeaderCell = TableHeaderRow.getElementsByTagName('th')[i];
            if (TableHeaderCell.innerText === "Title") {
                TableHeaderCell.setAttribute("onclick", "SortTable(\"" + TableID + "\", \"HTML\", " + i +")");
            }
            else if (TableHeaderCell.innerText === "Avg" || TableHeaderCell.innerText === "Pop") {
                TableHeaderCell.setAttribute("onclick", "SortTable(\"" + TableID + "\", \"Numeric\", " + i +")");
            }
            else {
                TableHeaderCell.setAttribute("onclick", "SortTable(\"" + TableID + "\", \"String\", " + i +")");
            }
        }
    }
}