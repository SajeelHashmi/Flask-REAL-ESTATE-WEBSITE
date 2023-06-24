/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      colors:{
        "primary": "#132F4C",
        "secondary":"#E9E9E9",
        "accent":"#FF9800",
  
      },
    
  },
  plugins: [],
}
}
