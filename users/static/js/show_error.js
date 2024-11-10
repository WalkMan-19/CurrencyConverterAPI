document.addEventListener("DOMContentLoaded", function() {
    const errorContainer = document.getElementById("errorContainer");
    if (errorContainer.innerHTML.trim() !== "") {
        errorContainer.classList.add("show");
    }
});
