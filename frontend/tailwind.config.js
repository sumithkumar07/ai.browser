/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ai-primary': '#8B5CF6',
        'ai-secondary': '#3B82F6',
        'ai-dark': '#0F172A',
        'ai-accent': '#06B6D4',
        gray: {
          50: '#F9FAFB',
          100: '#F3F4F6',
          200: '#E5E7EB',
          300: '#D1D5DB',
          400: '#9CA3AF',
          500: '#6B7280',
          600: '#4B5563',
          700: '#374151',
          800: '#1F2937',
          850: '#1A202C',
          900: '#111827',
          950: '#0D1117',
        },
        purple: {
          50: '#FAF5FF',
          100: '#F3E8FF',
          200: '#E9D5FF',
          300: '#D8B4FE',
          400: '#C084FC',
          500: '#A855F7',
          600: '#9333EA',
          700: '#7C2D12',
          800: '#581C87',
          900: '#3B0764',
        },
        blue: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          200: '#BFDBFE',
          300: '#93C5FD',
          400: '#60A5FA',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
          800: '#1E40AF',
          900: '#1E3A8A',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'Monaco', 'Consolas', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.75rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
        '6xl': ['3.75rem', { lineHeight: '1' }],
        '7xl': ['4.5rem', { lineHeight: '1' }],
        '8xl': ['6rem', { lineHeight: '1' }],
        '9xl': ['8rem', { lineHeight: '1' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
        '144': '36rem',
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
        'pulse-slow': 'pulse 3s ease-in-out infinite',
        'bounce-slow': 'bounce 3s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'slide-in-right': 'slide-in-right 0.4s ease-out',
        'slide-in-left': 'slide-in-left 0.4s ease-out',
        'fade-in-up': 'fade-in-up 0.6s ease-out',
        'scale-in': 'scale-in 0.3s ease-out',
        'ai-pulse': 'ai-pulse 2s infinite',
        'loading-dots': 'loading-dots 1.4s ease-in-out infinite both',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(-10px) rotate(1deg)' }
        },
        'slide-in-right': {
          'from': {
            transform: 'translateX(100%)',
            opacity: '0'
          },
          'to': {
            transform: 'translateX(0)',
            opacity: '1'
          }
        },
        'slide-in-left': {
          'from': {
            transform: 'translateX(-100%)',
            opacity: '0'
          },
          'to': {
            transform: 'translateX(0)',
            opacity: '1'
          }
        },
        'fade-in-up': {
          'from': {
            transform: 'translateY(30px)',
            opacity: '0'
          },
          'to': {
            transform: 'translateY(0)',
            opacity: '1'
          }
        },
        'scale-in': {
          'from': {
            transform: 'scale(0.8)',
            opacity: '0'
          },
          'to': {
            transform: 'scale(1)',
            opacity: '1'
          }
        },
        'ai-pulse': {
          '0%, 100%': { 
            boxShadow: '0 0 0 0 rgba(139, 92, 246, 0.7)'
          },
          '70%': { 
            boxShadow: '0 0 0 10px rgba(139, 92, 246, 0)'
          }
        },
        'loading-dots': {
          '0%, 80%, 100%': {
            transform: 'scale(0)',
            opacity: '0.5'
          },
          '40%': {
            transform: 'scale(1)',
            opacity: '1'
          }
        }
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'glass-strong': '0 8px 32px 0 rgba(31, 38, 135, 0.5)',
        'ai': '0 10px 30px -5px rgba(139, 92, 246, 0.4)',
        'ai-strong': '0 20px 40px -10px rgba(139, 92, 246, 0.5)',
        'neon': '0 0 20px rgba(139, 92, 246, 0.5)',
        'neon-strong': '0 0 40px rgba(139, 92, 246, 0.7)',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'ai-gradient': 'linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%)',
        'dark-gradient': 'linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%)',
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
      },
      backdropFilter: {
        'none': 'none',
        'blur': 'blur(20px)',
        'blur-sm': 'blur(10px)',
        'blur-lg': 'blur(40px)',
      },
      zIndex: {
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100',
        '150': '150',
        '200': '200',
      },
      transitionDuration: {
        '400': '400ms',
        '600': '600ms',
        '800': '800ms',
        '1200': '1200ms',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      scale: {
        '102': '1.02',
        '103': '1.03',
        '108': '1.08',
      },
      screens: {
        'xs': '475px',
        '3xl': '1600px',
        '4xl': '2000px',
      },
    },
  },
  plugins: [
    // Add custom utilities
    function({ addUtilities, theme }) {
      const newUtilities = {
        '.text-gradient': {
          'background': 'linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%)',
          '-webkit-background-clip': 'text',
          '-webkit-text-fill-color': 'transparent',
          'background-clip': 'text',
        },
        '.text-glow': {
          'text-shadow': '0 0 20px rgba(139, 92, 246, 0.5)',
        },
        '.glass': {
          'background': 'rgba(15, 23, 42, 0.8)',
          'backdrop-filter': 'blur(20px)',
          'border': '1px solid rgba(148, 163, 184, 0.1)',
        },
        '.glass-strong': {
          'background': 'rgba(15, 23, 42, 0.95)',
          'backdrop-filter': 'blur(40px)',
          'border': '1px solid rgba(148, 163, 184, 0.15)',
        },
        '.line-clamp-1': {
          'overflow': 'hidden',
          'display': '-webkit-box',
          '-webkit-box-orient': 'vertical',
          '-webkit-line-clamp': '1',
        },
        '.line-clamp-2': {
          'overflow': 'hidden',
          'display': '-webkit-box',
          '-webkit-box-orient': 'vertical',
          '-webkit-line-clamp': '2',
        },
        '.line-clamp-3': {
          'overflow': 'hidden',
          'display': '-webkit-box',
          '-webkit-box-orient': 'vertical',
          '-webkit-line-clamp': '3',
        },
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            'display': 'none',
          },
        },
      }
      addUtilities(newUtilities)
    },
  ],
}