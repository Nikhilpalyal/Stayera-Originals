document.querySelector('.scroll-container').addEventListener('wheel', function(event) {
    event.preventDefault();
    this.scrollLeft += event.deltaY;
});

document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".card");

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("fade-in");
            }
        });
    }, { threshold: 0.3 });

    cards.forEach(card => observer.observe(card));
});

