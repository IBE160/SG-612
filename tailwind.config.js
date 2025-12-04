/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./static/**/*.{html,js}",
    "./*.{html,js,py}",
    "./docs/**/*.{html,js}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#607AFB",
      },
      fontFamily: {
        display: ["Sora", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "0.5rem",
        lg: "1rem",
        xl: "1.5rem",
      },
    },
  },
  plugins: [],
}

