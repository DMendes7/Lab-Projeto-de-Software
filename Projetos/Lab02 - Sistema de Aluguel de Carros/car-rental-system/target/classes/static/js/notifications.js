(function () {
  function hide(el) {
    if (!el) return;
    el.style.animation = "toastOut .22s ease-in forwards";
    setTimeout(() => { el.style.display = "none"; }, 230);
  }
  document.addEventListener("click", function (e) {
    if (e.target.matches("[data-toast-close]")) {
      hide(e.target.closest(".notification"));
    }
  });
  document.querySelectorAll(".notification").forEach((el) => {
    el.classList.add("show");
    const dur = parseInt(el.getAttribute("data-duration") || "4000", 10);
    if (dur > 0) setTimeout(() => hide(el), dur);
  });
})();
