/**
 * LoomLuxe - Hero Slider JavaScript
 */
document.addEventListener('DOMContentLoaded', function() {
    const heroSlider = document.getElementById('heroSlider');
    if (!heroSlider) return;

    const slides = heroSlider.querySelectorAll('.hero-slide');
    if (slides.length <= 1) return;

    let currentSlide = 0;
    
    function nextSlide() {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
    }

    setInterval(nextSlide, 5000);
});
