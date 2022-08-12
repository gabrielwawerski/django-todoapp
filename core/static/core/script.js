const allCheckboxes = document.querySelectorAll(".checkbox");

for (let i = 0; i < allCheckboxes.length; i++) {
    allCheckboxes[i].addEventListener('click', () => {
        const completed = allCheckboxes[i].checked;
        const id = allCheckboxes[i].id;

        let data = {
            id: id,
            completed: completed
        };
        fetch("/", {
            method: 'POST',
            body: JSON.stringify(data)
        }).then(r => {return r.json()})
            .then(data => console.log(data))
    })
}
