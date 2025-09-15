/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  darkMode: "class",
  theme: {
    screens: {
      xl: "1440px",
      lg: "1280px",
      md: "1024px",
      sm: "768px"
    },
    extend: {
      colors: {
        bg: {
          canvas: "var(--bg-canvas)",
          card: "var(--bg-card)"
        },
        text: {
          primary: "var(--text-primary)",
          muted: "var(--text-muted)"
        },
        accent: {
          DEFAULT: "var(--accent)",
          hover: "var(--accent-hover)"
        },
        state: {
          success: "var(--state-success)",
          warning: "var(--state-warning)",
          danger: "var(--state-danger)",
          info: "var(--state-info)"
        },
        border: {
          DEFAULT: "var(--border)",
          muted: "var(--border-muted)"
        }
      },
      borderRadius: {
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
        xl: "var(--radius-xl)"
      },
      boxShadow: {
        elev0: "var(--shadow-0)",
        elev1: "var(--shadow-1)",
        elev2: "var(--shadow-2)",
        elev3: "var(--shadow-3)"
      },
      // Optional: keep Tailwind spacing defaults; add any bespoke steps here
      spacing: {
        // example custom steps aligned to your tokens
        4.5: "1.125rem",
        18: "4.5rem"
      },
      container: {
        center: true,
        padding: "1rem"
      }
    }
  },
  plugins: []
};
