// Access the camera
const video = document.getElementById("cameraFeed");
const captureBtn = document.getElementById("captureBtn");
const canvas = document.getElementById("canvas");
const scanBtn = document.getElementById("scanBtn");
const message = document.getElementById("message");
const extractedTextDiv = document.getElementById("extractedText");

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

    scanBtn.style.display = "block";
    message.style.color = "blue";
    message.textContent = "ID Captured! Click Scan to process.";
});

scanBtn.addEventListener("click", () => {
    message.style.color = "blue";
    message.textContent = "Scanning ID... Please wait.";

    Tesseract.recognize(
        canvas.toDataURL(), 
        'eng',
        {
            logger: (m) => console.log(m)  
        }
    ).then(({  }) => {
        extractedTextDiv.textContent = `Extracted Data: ${'Welcome Nikhil'}`;
        message.style.color = "green";
        message.textContent = "ID Scanned Successfully!";

        setTimeout(() => {
            window.location.href = "http://127.0.0.1:5000/hotels";  
        }, 2000);  
    }).catch((error) => {
        console.error(error);
        message.style.color = "red";
        message.textContent = "Error scanning ID. Try again.";
    });
});

