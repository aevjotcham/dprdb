document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-league-selector]").forEach((selector) => {
    selector.addEventListener("change", () => {
      window.location.assign(selector.value);
    });
  });
});
