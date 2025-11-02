/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')

module.exports = {
  // THIS IS THE FIX: Enable class-based dark mode
  darkMode: 'class',
  
  content: [
    './**/templates/**/*.html', // Scans all .html files
  ],
  theme: {
    extend: {
      colors: {
        // 'indigo' is our vibrant violet accent
        primary: colors.indigo,
        // 'slate' is our new, clean background for dark mode
        secondary: colors.slate, 
        success: colors.green,
        danger: colors.red,
        warning: colors.amber,
      },
      // --- "GOD-LEVEL" ANIMATIONS ---
      keyframes: {
        'fade-in-up': {
          '0%': {
            opacity: '0',
            transform: 'translateY(10px)'
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)'
          },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-3px)' },
        }
      },
      animation: {
        'fade-in-up': 'fade-in-up 0.5s ease-out forwards',
        'float': 'float 3s ease-in-out infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}