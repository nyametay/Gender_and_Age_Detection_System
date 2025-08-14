lucide.createIcons();
document.getElementById('themeToggle').addEventListener('click', () => {
  document.documentElement.classList.toggle('dark');
  localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  lucide.createIcons();
});