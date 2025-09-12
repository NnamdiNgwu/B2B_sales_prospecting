/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}", // Scan all React component files for classes
  ],
  darkMode: 'class', // Enable dark mode based on a class on the <html> tag
  theme: {
    extend: {
      colors: {
        // You can extend the default color palette here
        'primary': '#3490dc',
        'secondary': '#ffed4a',
        'danger': '#e3342f',
      },
      fontFamily: {
        // You can set custom fonts here
        sans: ['Inter', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'), // A plugin for better default form styles
  ],
}