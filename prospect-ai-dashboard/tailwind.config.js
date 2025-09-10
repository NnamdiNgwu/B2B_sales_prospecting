/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Scan all React component files for classes
  ],
  darkMode: 'class', // Enable dark mode based on a class on the <html> tag
  theme: {
    extend: {
      colors: {
        // You can extend the default color palette here
      },
      fontFamily: {
        // You can set custom fonts here
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'), // A plugin for better default form styles
  ],
}