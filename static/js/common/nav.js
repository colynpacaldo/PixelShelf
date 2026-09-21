document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("nav-toggle");
    const links = document.getElementById("nav-links");
    if (!toggle || !links) return;

    function setOpen(open) {
        links.classList.toggle("open", open);
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }

    toggle.addEventListener("click", function () {
        setOpen(!links.classList.contains("open"));
    });

    // Tapping a link (or navigating) closes the menu rather than leaving
    // it open behind the next page.
    links.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () { setOpen(false); });
    });

    // Tapping outside the open menu closes it.
    document.addEventListener("click", function (e) {
        if (!links.classList.contains("open")) return;
        if (links.contains(e.target) || toggle.contains(e.target)) return;
        setOpen(false);
    });

    // Resizing back to desktop width shouldn't leave the mobile panel
    // stuck open underneath the now-horizontal nav.
    window.addEventListener("resize", function () {
        if (window.innerWidth > 768) setOpen(false);
    });
});