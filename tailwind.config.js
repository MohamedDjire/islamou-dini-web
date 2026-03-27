/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1E40AF',
        secondary: '#0F766E',
        accent: '#DC2626',
        neutral: '#6B7280',
      },
    },
  },
  plugins: [],
}
