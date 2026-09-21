document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("register-form");
    var password = document.getElementById("password");
    var confirm = document.getElementById("confirm_password");
    var matchError = document.getElementById("match-error");

    if (!form || !password || !confirm) {
        return;
    }

    form.addEventListener("submit", function (event) {
        if (password.value !== confirm.value) {
            event.preventDefault();
            matchError.hidden = false;
        } else {
            matchError.hidden = true;
        }
    });
});
