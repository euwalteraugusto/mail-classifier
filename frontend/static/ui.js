document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#analysis-form");
    const textarea = document.querySelector("#email-text");
    const button = document.querySelector("#submit-btn");
    const btnText = document.querySelector("#btn-text");
    const loader = document.querySelector("#loader");
    const fileInput = document.querySelector("#file-input");
    const fileNameDisplay = document.querySelector("#file-name");

    // 1. Feedback de Seleção de Arquivo
    if (fileInput) {
        fileInput.addEventListener("change", (e) => {
            if (fileInput.files.length > 0) {
                const name = fileInput.files[0].name;
                const size = (fileInput.files[0].size / 1024).toFixed(1);
                fileNameDisplay.innerHTML = `📄 <b class="text-blue-400">${name}</b> (${size} KB)`;
                fileNameDisplay.parentElement.classList.add("border-blue-500", "bg-blue-500/5");
            } else {
                fileNameDisplay.textContent = "Arraste ou clique para PDF/TXT";
                fileNameDisplay.parentElement.classList.remove("border-blue-500", "bg-blue-500/5");
            }
        });
    }

    // 2. Estado de Carregamento no Submit
    if (form) {
        form.addEventListener("submit", () => {
            button.disabled = true;
            button.classList.add("opacity-80", "cursor-not-allowed");
            btnText.textContent = "IA Processando...";
            loader.classList.remove("hidden");
        });
    }

    // 3. Atalho Ctrl+Enter
    textarea.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && e.ctrlKey) {
            form.submit();
        }
    });
});