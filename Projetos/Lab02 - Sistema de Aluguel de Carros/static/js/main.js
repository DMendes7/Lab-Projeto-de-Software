// Toasts minimalistas
function createToast({ level = "info", text = "", timeout = 2800 }) {
  const root = document.getElementById("toast-root");
  if (!root) return;

  const el = document.createElement("div");
  el.className = `toast ${level}`;
  el.innerHTML = `
    <div style="display:flex; gap:10px; align-items:center;">
      <div style="font-weight:700; text-transform:capitalize">${level}</div>
      <div style="flex:1">${text}</div>
      <button class="close" aria-label="Fechar">&times;</button>
    </div>
  `;

  root.appendChild(el);
  const closer = el.querySelector(".close");
  const hide = () => { el.classList.add("toast-hide"); setTimeout(() => el.remove(), 220); };
  closer.addEventListener("click", hide);
  setTimeout(hide, timeout);
}

document.addEventListener("DOMContentLoaded", () => {
  // Converte mensagens do Django em toasts
  if (Array.isArray(window.__DJANGO_MESSAGES__)) {
    window.__DJANGO_MESSAGES__.forEach(m => {
      const level = m.level.includes("success") ? "success"
                   : m.level.includes("error") || m.level.includes("danger") ? "error"
                   : "info";
      createToast({ level, text: m.text });
    });
  }
});
