const video = document.getElementById("cameraFeed");
const captureBtn = document.getElementById("captureBtn");
const canvas = document.getElementById("canvas");
const registerBtn = document.getElementById("registerBtn");
const message = document.getElementById("message");

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing camera:", error);
        message.style.color = "red";
        message.textContent = "Camera access denied!";
    });

captureBtn.addEventListener("click", () => {
    const ctx = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    registerBtn.style.display = "block";
    message.style.color = "blue";
    message.textContent = "Face Captured! Enter Name and Click Register.";
});

registerBtn.addEventListener("click", () => {
    const name = prompt("Enter Your Name:");
    if (!name) {
        message.style.color = "red";
        message.textContent = "Registration canceled!";
        return;
    }

    const imageData = canvas.toDataURL("image/png");

    fetch("/register-face", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, image: imageData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            message.style.color = "green";
            message.textContent = "Face ID Registered Successfully!";
        } else {
            message.style.color = "red";
            message.textContent = data.message;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        message.style.color = "red";
        message.textContent = "An error occurred.";
    });
});
