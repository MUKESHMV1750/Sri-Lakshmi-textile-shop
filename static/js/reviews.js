/**
 * LoomLuxe - Reviews & Ratings JavaScript
 * Interactive star selection, review submission, and filter handling
 */

document.addEventListener('DOMContentLoaded', function () {
    initStarRatingInput();
    initReviewForm();
});

function initStarRatingInput() {
    const starContainer = document.querySelector('.star-rating-input');
    if (!starContainer) return;

    const stars = starContainer.querySelectorAll('i');
    const ratingInput = document.querySelector('#rating-val');

    stars.forEach((star, index) => {
        star.addEventListener('mouseenter', () => {
            highlightStars(stars, index + 1);
        });

        star.addEventListener('mouseleave', () => {
            const currentVal = parseInt(ratingInput.value) || 0;
            highlightStars(stars, currentVal);
        });

        star.addEventListener('click', () => {
            const selectedVal = index + 1;
            ratingInput.value = selectedVal;
            highlightStars(stars, selectedVal);
        });
    });
}

function highlightStars(stars, count) {
    stars.forEach((s, idx) => {
        if (idx < count) {
            s.classList.remove('far');
            s.classList.add('fas', 'active');
        } else {
            s.classList.remove('fas', 'active');
            s.classList.add('far');
        }
    });
}

function initReviewForm() {
    const reviewForm = document.querySelector('#add-review-form');
    if (!reviewForm) return;

    reviewForm.addEventListener('submit', function (e) {
        const ratingInput = document.querySelector('#rating-val');
        if (!ratingInput || !ratingInput.value || parseInt(ratingInput.value) === 0) {
            e.preventDefault();
            showToast('Please select a star rating before submitting.', 'info');
        }
    });
}
