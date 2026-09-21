document.addEventListener("DOMContentLoaded", function () {
    var darkModeCheckbox = document.querySelector("input[name='dark_mode']");

    if (!darkModeCheckbox) {
        return;
    }

    function applyPreview() {
        document.body.classList.toggle("dark-mode-preview", darkModeCheckbox.checked);
    }

    applyPreview();
    darkModeCheckbox.addEventListener("change", applyPreview);
});
