document.querySelectorAll(".toggle-password").forEach(button => {
    button.addEventListener("click", function () {
        const inputId = this.getAttribute("data-target");
        const input = document.getElementById(inputId);
        const icon = this.querySelector("svg");

        if (input.type === "password") {
            input.type = "text";
            icon.innerHTML = `
                <path d="M13.875 18.825A10.05 10.05 0 0112 19
                         c-4.478 0-8.268-2.943-9.542-7
                         1.001-3.192 3.64-5.62 6.875-6.58"/>
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path d="M3 3l18 18"/>`; // eye-off
        } else {
            input.type = "password";
            icon.innerHTML = `
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path d="M2.458 12C3.732 7.943 7.523 5
                         12 5c4.478 0 8.268 2.943 9.542 7
                         -1.274 4.057-5.064 7-9.542 7
                         -4.477 0-8.268-2.943-9.542-7z"/>`; // eye
        }
    });
});