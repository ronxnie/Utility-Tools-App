module.exports = {
  darkMode: "class",
  content: ["./app/templates/**/*.html", "./app/static/js/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      colors: {
        ink: "#101828",
        aqua: "#00A7B5",
        coral: "#FF6B5A",
        limepop: "#B7E85F"
      },
      boxShadow: {
        glow: "0 20px 60px rgba(0, 167, 181, .22)"
      }
    }
  },
  plugins: [require("@tailwindcss/forms")]
};
