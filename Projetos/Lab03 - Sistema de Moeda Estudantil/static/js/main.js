// Mensagens flash simples (placeholder)
document.addEventListener("DOMContentLoaded", () => {
  const flashes = document.querySelectorAll("[data-flash]");
  flashes.forEach(el => setTimeout(() => el.remove(), 5000));
});
