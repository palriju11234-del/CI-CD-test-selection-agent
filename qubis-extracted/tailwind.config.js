/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        tm: {
          orange: '#D35C07',
          amber: '#FEB048',
          surface: '#F5F5F5',
          card: '#D9D9D9',
          muted: '#666666',
          dark: '#111111',
        },
      },
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
        orbitron: ['Orbitron', 'sans-serif'],
      },
      boxShadow: {
        'btn-orange': '0 5px 31.9px 6px rgba(0,0,0,0.25), 0 4px 6.2px rgba(0,0,0,0.25), inset 0 6px 11.1px rgba(0,0,0,0.25)',
        'btn-demo': '0 5px 31.9px 6px rgba(0,0,0,0.25), 0 4px 6.2px rgba(0,0,0,0.25), inset 0 6px 11.1px rgba(0,0,0,0.25)',
        'card-inset': 'inset -4px -5px 18px rgba(0,0,0,0.25), inset 4px 4px 18px rgba(0,0,0,0.27)',
      },
      screens: {
        'xs': '480px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1440px',
      },
    },
  },
  plugins: [],
}
