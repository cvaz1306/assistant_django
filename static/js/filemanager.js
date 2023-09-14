const fileList = document.getElementById("files");
// Create a function to generate a rounded square card
function createRoundedSquareCard(link, title, text) {
    const card = document.createElement("a");
    card.href = link;
    card.classList.add("card");

    const cardContent = document.createElement("div");
    cardContent.classList.add("card-content");

    const heading = document.createElement("h2");
    heading.textContent = title;

    const paragraph = document.createElement("p");
    paragraph.textContent = text;

    cardContent.appendChild(heading);
    cardContent.appendChild(paragraph);

    card.appendChild(cardContent);

    return card;
}

// Append the card to the container


var d;

function updateFiles() {
    fetch('/filemanager/files').then(response => response.json()).then(data => {
        console.log(data);
        d = data;
        const fx = document.createElement('div');

        data.forEach(item => {

            const card = createRoundedSquareCard("/filemanager/get?id=" + item.id.toString(), item.name.slice(0, 8) + "...", "Download");
            fx.appendChild(card);
        });
        fileList.innerHTML = fx.innerHTML;
        fx.innerHTML = "";
    })
}
let e = false;
const form = document.getElementById("fileX");
document.addEventListener('submit', (e) => {
    e.preventDefault();
    // Store reference to form to make later code easier to read
    const form = e.target;

    // Post data using the Fetch API
    fetch(form.action, {
        method: form.method,
        body: new FormData(form),
    });

    // Prevent the default form submit

});
// Trigger file input click when the plus button is clicked
const uploadButton = document.querySelector('.upload-button');
const fileInput = document.getElementById('file-input');
fileInput.addEventListener('click', (event) => {
    if (!e) {
        event.preventDefault()
    }
    console.log("Clicked")

})
uploadButton.addEventListener('click', () => {
    e = true;
    console.log("Clicked button")
    fileInput.click();
    e = false;
    updateFiles();
});

// Prevent Enter key from triggering file input click
uploadButton.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
});

// Handle file selection (you can add further logic here)
fileInput.addEventListener('change', () => {
    // You can access selected file(s) via fileInput.files
    const selectedFile = fileInput.files[0];
    if (selectedFile) {
        // Handle the selected file, e.g., upload it to the server
        console.log(`Selected file: ${selectedFile.name}`);
        document.getElementById("sub").click();
    }
    updateFiles();
});
document.addEventListener('submit', (e) => {
    e.preventDefault();
    console.log("Sending");
    // Store reference to form to make later code easier to read
    const form = e.target;

    // Post data using the Fetch API
    fetch(form.action, {
        method: form.method,
        body: new FormData(form),
    });

    // Prevent the default form submit
    updateFiles();
});