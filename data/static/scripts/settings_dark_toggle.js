document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("darkModeToggle");
    const html = document.documentElement;

    // Apply saved preference on load
    if (localStorage.getItem("theme") === "dark" ||
        (!localStorage.getItem("theme") && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
        html.classList.add("dark");
        toggle.checked = true;
    } else {
        html.classList.remove("dark");
        toggle.checked = false;
    }

    // Toggle event
    toggle.addEventListener("change", () => {
        if (toggle.checked) {
            html.classList.add("dark");
            localStorage.setItem("theme", "dark");
        } else {
            html.classList.remove("dark");
            localStorage.setItem("theme", "light");
        }
    });
});
