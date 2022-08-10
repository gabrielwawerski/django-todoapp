let todoList = document.querySelector(`[id^="listid"]`);
let entries = document.getElementsByClassName("checkbox");
let entriesSpans = document.getElementsByClassName("span");
let editButtons = document.getElementsByClassName("btn");
let url = new URL(window.location.href).toString();
console.log(url);

for (let i = 0; i < entries.length; i++) {
    editButtons[i].addEventListener('click', () => {

        if (editButtons[i].getAttribute("value") === "Edit") {
            entriesSpans[i].innerHTML = `<input value="${entriesSpans[i].textContent}" id="changed${i}"/>`;
            editButtons[i].setAttribute("value", "Save");
        }

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
            }).then(r => {return r.json()})
                .then(data => {
                    // update entry text directly from response data.
                    entriesSpans[i].innerHTML = `<span>${data.entry_text}</span>`;
                });

            editButtons[i].setAttribute("value", "Edit");
        }
    });
}
