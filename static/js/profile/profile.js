document.addEventListener("DOMContentLoaded", function () {
    var fileInput = document.getElementById("id_profile_image");
    var preview = document.getElementById("profile-preview");
    var removeInput = document.getElementById("remove_profile_image");
    var removeButton = document.getElementById("remove-profile-image");
    var bioInput = document.getElementById("id_bio");
    var bioCounter = document.getElementById("bio-counter");

    if (fileInput && preview) {
        var originalPreview = preview.src;

        fileInput.addEventListener("change", function () {
            var file = fileInput.files && fileInput.files[0];
            if (!file) {
                return;
            }
            if (removeInput) {
                removeInput.checked = false;
            }
            if (removeButton) {
                removeButton.textContent = "Remove";
            }
            var reader = new FileReader();
            reader.onload = function (event) {
                preview.src = event.target.result;
            };
            reader.readAsDataURL(file);
        });

        if (removeButton && removeInput) {
            removeButton.addEventListener("click", function () {
                removeInput.checked = !removeInput.checked;
                preview.src = removeInput.checked
                    ? preview.dataset.defaultSrc
                    : originalPreview;
                removeButton.textContent = removeInput.checked ? "Undo Remove" : "Remove";
            });
        }
    }

    if (bioInput && bioCounter) {
        var updateBioCounter = function () {
            bioCounter.textContent = bioInput.value.length + " / 200";
        };
        bioInput.addEventListener("input", updateBioCounter);
        updateBioCounter();
    }
});
