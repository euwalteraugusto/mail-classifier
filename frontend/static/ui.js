document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.querySelector("#email-text");
    const button = document.querySelector("#submit-btn");
    const resultCard = document.querySelector(".result-card");
    const badge = document.querySelector(".badge");
    const reply = document.querySelector(".reply");
    const fileInput = document.querySelector("#file-input");
    const uploadLabel = document.querySelector(".file-upload span");

    if (!textarea || !button) return;

    /* ---------- Estado de carregamento ---------- */
    function setLoading(isLoading) {
        button.disabled = isLoading;
        button.textContent = isLoading ? "Processando..." : "Analisar";
    }

    /* ---------- Validação visual ---------- */
    textarea.addEventListener("input", () => {
        textarea.style.borderColor =
            textarea.value.trim().length < 10
                ? "#dc2626"
                : "var(--primary)";
    });

    /* ---------- Upload feedback ---------- */
    if (fileInput && uploadLabel) {
        fileInput.addEventListener("change", () => {
            uploadLabel.textContent =
                fileInput.files.length > 0
                    ? fileInput.files[0].name
                    : "Selecionar arquivo";
        });
    }

    /* ---------- Animação do resultado ---------- */
    function showResult() {
        if (!resultCard) return;

        resultCard.style.display = "block";
        resultCard.style.opacity = "0";
        resultCard.style.transform = "translateY(8px)";

        requestAnimationFrame(() => {
            resultCard.style.transition = "all 0.35s ease";
            resultCard.style.opacity = "1";
            resultCard.style.transform = "translateY(0)";
        });

        resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    /* ---------- Simulação de ciclo de UX ---------- */
    button.addEventListener("click", () => {
        setLoading(true);

        setTimeout(() => {
            setLoading(false);
            showResult();
        }, 600);
    });

    /* ---------- Acessibilidade ---------- */
    textarea.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && e.ctrlKey) {
            button.click();
        }
    });
});
