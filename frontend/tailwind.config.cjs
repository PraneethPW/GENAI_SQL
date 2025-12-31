module.exports = {
    theme: {
      extend: {
        keyframes: {
          'gradient-shift': {
            '0%, 100%': { backgroundPosition: '0% 50%' },
            '50%': { backgroundPosition: '100% 50%' },
          },
        },
        animation: {
          'gradient-shift': 'gradient-shift 20s ease infinite',
        },
      },
    },
    plugins: [],
  };
  