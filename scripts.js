
document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript loaded!");

    const form = document.querySelector("form");
    const inputs = form.querySelectorAll("input[type='number']");

    form.addEventListener("submit", (event) => {
        let isValid = true;

        inputs.forEach(input => {
            if (input.value === "" || isNaN(input.value) || input.value < 0) {
                isValid = false;
                input.classList.add("error");
            } else {
                input.classList.remove("error");
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert("Please fill out all fields with valid values!");
        }
    });

    const links = document.querySelectorAll("nav a");
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add("active");
        }
    });
});


function loadUnsplashImage(query, elementId) {
    const unsplashKey = 'zLACYwfqOgNVULSzFyMzM5v7G_oRtvB-39_CihiVRc8'; 
    const url = `https://api.unsplash.com/photos/random?query=${query}&client_id=${unsplashKey}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const imageElement = document.getElementById(elementId);
            if (imageElement && data.urls && data.urls.small) {
                imageElement.src = data.urls.small;
                imageElement.alt = query;
            } else {
                console.error("Image data not found.");
            }
        })
        .catch(error => {
            console.error("Error fetching Unsplash image:", error);
        });
}


