/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ai-primary': '#6366f1',
        'ai-secondary': '#8b5cf6',
        'ai-accent': '#06b6d4',
        'ai-dark': '#0f172a',
        'ai-light': '#f8fafc',
        'bubble': {
          100: '#f0f9ff',
          500: '#0ea5e9',
          700: '#0369a1',
          900: '#0c4a6e'
        }
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite alternate',
        'bubble-pop': 'bubble-pop 0.3s ease-out',
        'tab-slide': 'tab-slide 0.5s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'pulse-glow': {
          '0%': { boxShadow: '0 0 5px #6366f1' },
          '100%': { boxShadow: '0 0 20px #6366f1, 0 0 30px #6366f1' },
        },
        'bubble-pop': {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.1)' },
          '100%': { transform: 'scale(1)' },
        },
        'tab-slide': {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        }
      },
      backdropBlur: {
        xs: '2px',
      },
      fontFamily: {
        'ai': ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}