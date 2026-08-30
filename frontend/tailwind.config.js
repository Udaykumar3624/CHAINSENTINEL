/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#090d16',
        card: '#0f172a',
        border: '#1e293b',
        muted: '#64748b',
        primary: {
          DEFAULT: '#38bdf8',
          hover: '#0284c7',
        },
        risk: {
          low: '#10b981',
          medium: '#f59e0b',
          high: '#ef4444',
          critical: '#a855f7',
        }
      },
    },
  },
  plugins: [],
}
