const root = document.documentElement;
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
  root.classList.add("dark");
}

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    toggle.addEventListener("click", () => {
      root.classList.toggle("dark");
      localStorage.setItem("theme", root.classList.contains("dark") ? "dark" : "light");
    });
  }

  if (window.anime) {
    anime({
      targets: ".hero-chip",
      translateY: [-8, 0],
      opacity: [0, 1],
      delay: anime.stagger(90),
      easing: "easeOutExpo",
      duration: 900
    });
    anime({
      targets: ".tool-card",
      translateY: [16, 0],
      opacity: [0, 1],
      delay: anime.stagger(45),
      easing: "easeOutExpo",
      duration: 700
    });
  }
});
