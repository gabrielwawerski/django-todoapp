let todoList = document.querySelector(`[id^="listid"]`);
let entries = document.getElementsByClassName("checkbox");
let entriesSpans = document.getElementsByClassName("span");
let editButtons = document.getElementsByClassName("edit btn");
let url = new URL(window.location.href).toString();
console.log(url);

// check if edit buttons exist; buttons are hidden if not logged in (prevents console error)
if (editButtons.length !== 0) {
    for (let i = 0; i < entries.length; i++) {
        editButtons[i].addEventListener('click', () => {
            // if Edit is the buttons value, replace entry's span with input field
            if (editButtons[i].getAttribute("value") === "🖉") {
                entriesSpans[i].innerHTML = `<input value="${entriesSpans[i].textContent}" id="changed${i}"/>`;
                editButtons[i].setAttribute("value", "Save");
            }

            // get input value, query db, replace input with span and updated text
            else if (editButtons[i].getAttribute("value") === "Save") {
                const entry_text = document.getElementById(`changed${i}`).value;
                const data = {
                    action: "edit_entry",
                    entry_id: entries[i].id,
                    entry_text: entry_text,
                };

                fetch(url, {
                    method: 'POST',
                    body: JSON.stringify(data)
                }).then(r => {
                    return r.json()
                }).then(data => {
                        // update entry text directly from response data.
                        entriesSpans[i].innerHTML = `<span>${data.entry_text}</span>`;
                        editButtons[i].setAttribute("value", "🖉");
                    });
            }
        });
    }
}

function editList(id) {
    let editButton = document.getElementsByClassName("list-edit");
    let h3 = document.getElementsByClassName("h3name");
    h3 = h3[0];
    editButton = editButton[0];

    if (editButton.getAttribute("value") === "🖉") {
        h3.innerHTML = `<input value="${h3.textContent}" id="changed-title"/>`;
        editButton.setAttribute("value", "Save");
    }

    else if (editButton.getAttribute("value") === "Save") {
        const list_name = document.getElementById(`changed-title`).value;
        const data = {
            action: "edit_list_name",
            list_id: id,
            list_name: list_name,
        };

        fetch(url, {
            method: 'POST',
            body: JSON.stringify(data)
        }).then(r => {
            return r.json()
        }).then(data => {
            // update entry text directly from response data.
            h3.innerHTML = `<span>${data.list_name}</span>`;
            editButton.setAttribute("value", "🖉");
        });
    }
}

// delete list's entry when button pressed
function delEntry(id) {
    console.log("delEntry!");
    const data = {
        action: "delete_entry",
        entry_id: id
    };

    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data)
    }).then(r => {
        return r.json()
    }).then(data => {
            document.getElementById(`li-entry${id}`).remove();
        });
}

function delContributor(id) {
    console.log("del contributor!");
    const data = {
        action: 'delete_contributor',
        contributor_id: id
    };

    fetch(url, {
        method: 'POST',
        body: JSON.stringify(data)
    }).then(r => {
        return r.json()
    }).then(data => {
        document.getElementById(`contributor${id}`).remove();
        document.getElementById(`contributor-remove-button${id}`).remove();
        window.location.reload();
    });
}
