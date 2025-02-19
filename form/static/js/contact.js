const inputs = document.querySelectorAll(".input");
const form = document.querySelector("form");

function focusFunc() {
  let parent = this.parentNode;
  parent.classList.add("focus");
}

function blurFunc() {
  let parent = this.parentNode;
  if (this.value == "") {
    parent.classList.remove("focus");
  }
}

inputs.forEach((input) => {
  input.addEventListener("focus", focusFunc);
  input.addEventListener("blur", blurFunc);
});

// Form submission event
form.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent default form submission
  alert("Your message has been sent successfully!");
  
  // Optionally, reset the form fields
  form.reset();

  // Remove focus styles
  inputs.forEach((input) => {
    let parent = input.parentNode;
    parent.classList.remove("focus");
  });
});
