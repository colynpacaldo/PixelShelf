document.addEventListener("DOMContentLoaded", function () {
    var toggleBtn = document.getElementById("toggle-password");
    var passwordInput = document.getElementById("password");

    if (!toggleBtn || !passwordInput) {
        return;
    }

    toggleBtn.addEventListener("click", function () {
        var isHidden = passwordInput.type === "password";
        passwordInput.type = isHidden ? "text" : "password";
        toggleBtn.textContent = isHidden ? "Hide" : "Show";
    });
});
