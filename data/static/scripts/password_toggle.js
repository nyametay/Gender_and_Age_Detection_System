const toggleBtn = document.getElementById('toggle-password');
const passwordInput = document.getElementById('password');
const eyeIcon = document.getElementById('eye-icon');

toggleBtn.addEventListener('click', () => {
  const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
  passwordInput.setAttribute('type', type);

  // Toggle the icon (optional: change between eye/eye-off)
  if (type === 'text') {
    eyeIcon.innerHTML = `<path d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.96 9.96 0 012.847-4.419M6.32 6.318A9.953 9.953 0 0112 5c4.477 0 8.268 2.943 9.542 7a9.957 9.957 0 01-4.254 5.136M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M3 3l18 18" stroke-linecap="round" stroke-linejoin="round"/>`;
  } else {
    eyeIcon.innerHTML = `<path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>`;
  }
});