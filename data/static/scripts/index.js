const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const placeholder = document.getElementById("placeholder");

const webcamBtn = document.getElementById("webcamBtn");
const webcamModal = document.getElementById("webcamModal");
const video = document.getElementById("webcam");
const canvas = document.getElementById("canvas");
const captureBtn = document.getElementById("captureBtn");
const closeModal = document.getElementById("closeModal");
const webcamImageInput = document.getElementById("webcamImage");

// ---- File Upload Preview ----
fileInput.addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            preview.src = event.target.result;
            preview.classList.remove("hidden");
            placeholder.classList.add("hidden");
        };
        reader.readAsDataURL(file);
    }
});

// ---- Webcam Handling ----
let stream;

webcamBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    webcamModal.classList.remove("hidden");

    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (err) {
        console.error("Webcam access denied:", err);
    }
});

closeModal.addEventListener("click", () => {
    webcamModal.classList.add("hidden");
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});

// ---- Capture Photo ----
captureBtn.addEventListener("click", () => {
    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataURL = canvas.toDataURL("image/jpeg");
    preview.src = dataURL;
    preview.classList.remove("hidden");
    placeholder.classList.add("hidden");

    webcamImageInput.value = dataURL;

    // Close modal + stop webcam
    webcamModal.classList.add("hidden");
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});
