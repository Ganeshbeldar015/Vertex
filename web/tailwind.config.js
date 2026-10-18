/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        maroon: {
          50: "#fdf2f4",
          100: "#fbe8eb",
          200: "#f7d0d8",
          300: "#efa9b8",
          400: "#e4758d",
          500: "#d44766",
          600: "#b92548",
          700: "#9c1737",
          800: "#800020",
          900: "#68001a",
          950: "#3b000d",
        },
        obsidian: {
          950: "#070709",
          900: "#0c0c10",
          850: "#121218",
          800: "#181822",
          750: "#20202c",
          700: "#2a2a3a",
        },
      },
      boxShadow: {
        "maroon-glow": "0 0 20px -3px rgba(128, 0, 32, 0.4)",
        "maroon-subtle": "0 0 12px 0 rgba(128, 0, 32, 0.25)",
      },
    },
  },
  plugins: [],
};
