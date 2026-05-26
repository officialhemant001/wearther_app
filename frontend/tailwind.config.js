/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Outfit', 'sans-serif'],
      },
      colors: {
        brand: {
          50: '#f5f8ff',
          100: '#ebf1fe',
          200: '#dde7fe',
          300: '#c4d5fd',
          400: '#a3beeb',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#0f172a',
        },
        accent: {
          amber: '#f59e0b',
          emerald: '#10b981',
          rose: '#f43f5e',
          cyan: '#06b6d4',
          indigo: '#6366f1',
        },
        slate: {
          950: '#0b0f19', // deep premium dark background
        }
      },
      boxShadow: {
        'premium': '0 4px 30px rgba(0, 0, 0, 0.03)',
        'premium-hover': '0 10px 40px rgba(0, 0, 0, 0.08)',
        'card-dark': '0 4px 30px rgba(0, 0, 0, 0.4)',
        'glow-cyan': '0 0 20px rgba(6, 182, 212, 0.15)',
        'glow-amber': '0 0 20px rgba(245, 158, 11, 0.15)',
      },
      borderWidth: {
        '0.5': '0.5px',
      },
    },
  },
  plugins: [],
}
