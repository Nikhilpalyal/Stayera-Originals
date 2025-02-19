document.addEventListener("DOMContentLoaded", () => {
    const flipCheckbox = document.getElementById("flip");
    const signupForm = document.querySelector(".signup-form form");
    const loginForm = document.querySelector(".login-form form");

    // Ensure signup is shown first by setting flip unchecked initially
    flipCheckbox.checked = false;

    // Toggle login/signup when clicking on the text
    document.getElementById("loginToggle").addEventListener("click", () => {
        flipCheckbox.checked = true;
    });

    document.getElementById("signupToggle").addEventListener("click", () => {
        flipCheckbox.checked = false;
    });

    // Signup event
    signupForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const name = signupForm.querySelector("input[placeholder='Enter your name']").value;
        const email = signupForm.querySelector("input[placeholder='Enter your email']").value;
        const password = signupForm.querySelector("input[placeholder='Enter your password']").value;

        if (name && email && password) {
            localStorage.setItem("user", JSON.stringify({ name, email, password }));
            alert("Signup successful! You can now log in.");
            flipCheckbox.checked = true; // Flip to login
        } else {
            alert("Please fill in all fields.");
        }
    });

    // Login event
    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const email = loginForm.querySelector("input[placeholder='Enter your email']").value;
        const password = loginForm.querySelector("input[placeholder='Enter your password']").value;
        const storedUser = JSON.parse(localStorage.getItem("user"));

        if (storedUser && storedUser.email === email && storedUser.password === password) {
            alert(`Welcome back, ${storedUser.name}! Login successful.`);
        } else {
            alert("Invalid email or password. Please try again.");
        }
    });
});
