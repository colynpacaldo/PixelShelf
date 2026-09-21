document.addEventListener("DOMContentLoaded", function () {
    var fileInput = document.querySelector("input[type='file']");
    var preview = document.getElementById("profile-preview");

    if (!fileInput || !preview) {
        return;
    }

    fileInput.addEventListener("change", function () {
        var file = fileInput.files && fileInput.files[0];
        if (!file) {
            return;
        }
        var reader = new FileReader();
        reader.onload = function (event) {
            preview.src = event.target.result;
        };
        reader.readAsDataURL(file);
    });
});
