// Automatically hide flash messages after 10 seconds
 setTimeout(() => {
    document.querySelectorAll('.flash-msg').forEach(msg => {
      msg.classList.add('opacity-0', 'transition-opacity', 'duration-500');
      setTimeout(() => msg.remove(), 500);
    });
 }, 3000); // 3 seconds