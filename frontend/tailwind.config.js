/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          950: '#082f49',
        },
        dark: {
          bg: '#0f172a',
          card: '#1e293b',
          border: '#334155',
          text: '#f8fafc',
          muted: '#94a3b8'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      keyframes: {
        'fade-in':   { '0%': { opacity: '0', transform: 'translateY(10px)' }, '100%': { opacity: '1', transform: 'translateY(0)' } },
        'slide-in':  { '0%': { opacity: '0', transform: 'translateX(-20px)' }, '100%': { opacity: '1', transform: 'translateX(0)' } },
        'scale-in':  { '0%': { opacity: '0', transform: 'scale(0.95)' }, '100%': { opacity: '1', transform: 'scale(1)' } },
        'float':     { '0%, 100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-5px)' } },
        'pulse-glow':{ '0%, 100%': { opacity: '1', boxShadow: '0 0 10px rgba(14, 165, 233, 0.2)' }, '50%': { opacity: '0.9', boxShadow: '0 0 20px rgba(14, 165, 233, 0.4)' } },
      },
      animation: {
        'fade-in':  'fade-in 0.4s ease-out forwards',
        'slide-in': 'slide-in 0.3s ease-out forwards',
        'scale-in': 'scale-in 0.3s ease-out forwards',
        'float':    'float 4s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 3s infinite',
      },
    },
  },
  plugins: [],
};
