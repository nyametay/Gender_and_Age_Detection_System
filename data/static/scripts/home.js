// static/scripts/home.js
document.addEventListener('DOMContentLoaded', () => {
  // Safe lucide init (won't throw if lucide is missing)
  if (window.lucide && typeof lucide.createIcons === 'function') {
    lucide.createIcons();
  } else {
    console.warn('lucide not available — icons may not render.');
  }

  const safeOn = (id, evt, fn) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener(evt, fn);
    return el;
  };

  // Theme toggle logic (desktop & mobile)
  const toggleDarkMode = () => {
    document.documentElement.classList.toggle('dark');
    try { localStorage.theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light'; } catch (e) { /* ignore */ }
    if (window.lucide && typeof lucide.createIcons === 'function') lucide.createIcons();
  };
  safeOn('themeToggle', 'click', toggleDarkMode);
  safeOn('themeToggleMobile', 'click', toggleDarkMode);

  // Mobile menu toggle
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
  }

  // Profile dropdown toggle
  const userAvatar = document.getElementById('userAvatar');
  const userDropdown = document.getElementById('userDropdown');
  if (userAvatar && userDropdown) {
    userAvatar.addEventListener('click', (e) => {
      e.stopPropagation(); // prevent the document click handler from immediately closing it
      userDropdown.classList.toggle('hidden');
    });

    // Close dropdown if clicking outside
    document.addEventListener('click', (event) => {
      if (!userAvatar.contains(event.target) && !userDropdown.contains(event.target)) {
        userDropdown.classList.add('hidden');
      }
    });
  }

  console.log('home.js loaded and listeners attached (if elements exist).');
});
