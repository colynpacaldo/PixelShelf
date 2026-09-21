document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".remove-from-shelf-form").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!confirm("Remove this asset from the shelf?")) {
                event.preventDefault();
            }
        });
    });
});
