// Preview uploaded image
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const placeholder = document.getElementById('placeholder');

fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      preview.src = reader.result;
      preview.classList.remove('hidden');
      placeholder.classList.add('hidden');
    };
    reader.readAsDataURL(file);
  }
});