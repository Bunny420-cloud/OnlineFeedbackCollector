/**
 * Online Feedback Collector - JavaScript Application Logic
 * Features: Interactive star rating, Client-side validation, AJAX submit, Chart.js rendering, Table search.
 */

document.addEventListener("DOMContentLoaded", () => {
    initStarRatingWidget();
    initFeedbackFormValidation();
    initAdminDashboard();
});

/* ==========================================================================
   1. INTERACTIVE STAR RATING WIDGET
   ========================================================================== */
function initStarRatingWidget() {
    const starInputs = document.querySelectorAll('.star-rating-wrapper input[type="radio"]');
    const previewLabel = document.getElementById('ratingPreviewLabel');

    if (!starInputs.length || !previewLabel) return;

    const ratingDescriptions = {
        '1': '★☆☆☆☆ (1/5) - Poor',
        '2': '★★☆☆☆ (2/5) - Fair',
        '3': '★★★☆☆ (3/5) - Good',
        '4': '★★★★☆ (4/5) - Very Good',
        '5': '★★★★★ (5/5) - Excellent'
    };

    starInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const val = e.target.value;
            previewLabel.textContent = ratingDescriptions[val] || `${val} Stars`;
            previewLabel.classList.add('animate__animated', 'animate__pulse');
            setTimeout(() => previewLabel.classList.remove('animate__pulse'), 500);
        });
    });
}

/* ==========================================================================
   2. CLIENT-SIDE VALIDATION & AJAX SUBMISSION
   ========================================================================== */
function initFeedbackFormValidation() {
    const form = document.getElementById('feedbackForm');
    const alertBox = document.getElementById('formAlertBox');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideAlert();

        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        const commentsInput = document.getElementById('comments');
        const ratingSelected = document.querySelector('.star-rating-wrapper input[type="radio"]:checked');

        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const comments = commentsInput.value.trim();
        const rating = ratingSelected ? ratingSelected.value : null;

        // Validation Rules
        if (!name) {
            showAlert('Please enter your full name.', 'danger');
            nameInput.focus();
            return;
        }
        if (name.length < 2) {
            showAlert('Name must be at least 2 characters long.', 'danger');
            nameInput.focus();
            return;
        }

        if (!email) {
            showAlert('Please enter your email address.', 'danger');
            emailInput.focus();
            return;
        }

        const emailRegex = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
        if (!emailRegex.test(email)) {
            showAlert('Please enter a valid email address (e.g. name@domain.com).', 'danger');
            emailInput.focus();
            return;
        }

        if (!rating) {
            showAlert('Please select a star rating from 1 to 5.', 'danger');
            return;
        }

        if (!comments) {
            showAlert('Please enter your feedback comments.', 'danger');
            commentsInput.focus();
            return;
        }
        if (comments.length < 5) {
            showAlert('Feedback comments must be at least 5 characters long.', 'danger');
            commentsInput.focus();
            return;
        }

        // Show submit loading state
        const submitBtn = document.getElementById('submitBtn');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Submitting...`;

        try {
            const response = await fetch('/submit-feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    rating: parseInt(rating),
                    comments: comments
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                showAlert(result.message || 'Thank you! Your feedback has been submitted successfully.', 'success');
                form.reset();
                
                // Reset preview text
                const previewLabel = document.getElementById('ratingPreviewLabel');
                if (previewLabel) previewLabel.textContent = 'Select 1-5 Stars';

                // Scroll to alert box smoothly
                alertBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                showAlert(result.error || 'Failed to submit feedback. Please check your inputs.', 'danger');
            }
        } catch (error) {
            console.error('Submission Error:', error);
            showAlert('A network error occurred while submitting feedback. Please try again.', 'danger');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });

    function showAlert(message, type) {
        if (!alertBox) return;
        alertBox.className = `alert-custom alert-${type}-custom mb-4`;
        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
        alertBox.innerHTML = `<i class="fas ${icon} fa-lg"></i> <div>${message}</div>`;
        alertBox.classList.remove('d-none');
    }

    function hideAlert() {
        if (!alertBox) return;
        alertBox.classList.add('d-none');
    }
}

/* ==========================================================================
   3. ADMIN DASHBOARD CHARTS & REAL-TIME SEARCH
   ========================================================================== */
function initAdminDashboard() {
    const ratingChartCanvas = document.getElementById('ratingDistributionChart');
    const trendChartCanvas = document.getElementById('feedbackTrendChart');
    const tableSearchInput = document.getElementById('tableSearchInput');

    // Only run if on admin dashboard page
    if (!ratingChartCanvas || !trendChartCanvas) return;

    fetchAndRenderDashboardCharts(ratingChartCanvas, trendChartCanvas);

    // Setup live search on feedback table
    if (tableSearchInput) {
        tableSearchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const tableRows = document.querySelectorAll('#feedbackTableBody tr');

            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
}

async function fetchAndRenderDashboardCharts(ratingCanvas, trendCanvas) {
    try {
        const response = await fetch('/api/feedback');
        const data = await response.json();

        if (!data.success || !data.feedback) return;

        const feedbackList = data.feedback;

        // 1. Calculate Rating Distribution (1 to 5 Stars)
        const ratingCounts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
        feedbackList.forEach(item => {
            const r = parseInt(item.rating);
            if (ratingCounts[r] !== undefined) ratingCounts[r]++;
        });

        // Render Rating Distribution Bar/Doughnut Chart
        new Chart(ratingCanvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                datasets: [{
                    label: 'Feedback Count',
                    data: [
                        ratingCounts[1],
                        ratingCounts[2],
                        ratingCounts[3],
                        ratingCounts[4],
                        ratingCounts[5]
                    ],
                    backgroundColor: [
                        '#f43f5e',
                        '#fb923c',
                        '#facc15',
                        '#38bdf8',
                        '#10b981'
                    ],
                    borderRadius: 8,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#0f172a',
                        titleFont: { family: 'Plus Jakarta Sans', weight: 'bold' },
                        bodyFont: { family: 'Plus Jakarta Sans' },
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#94a3b8', stepSize: 1 },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    },
                    x: {
                        ticks: { color: '#94a3b8' },
                        grid: { display: false }
                    }
                }
            }
        });

        // 2. Calculate Submission Trend over Dates
        const dateCountsMap = {};
        feedbackList.forEach(item => {
            // Extract YYYY-MM-DD
            const dateStr = item.date_submitted ? item.date_submitted.split(' ')[0] : 'Unknown';
            dateCountsMap[dateStr] = (dateCountsMap[dateStr] || 0) + 1;
        });

        // Sort dates chronologically
        const sortedDates = Object.keys(dateCountsMap).sort();
        const trendValues = sortedDates.map(d => dateCountsMap[d]);

        // Render Submission Trend Line Chart
        new Chart(trendCanvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: sortedDates.length ? sortedDates : ['No Data'],
                datasets: [{
                    label: 'Submissions',
                    data: trendValues.length ? trendValues : [0],
                    borderColor: '#818cf8',
                    backgroundColor: 'rgba(129, 140, 248, 0.15)',
                    fill: true,
                    tension: 0.35,
                    pointRadius: 5,
                    pointBackgroundColor: '#c084fc',
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#0f172a',
                        titleFont: { family: 'Plus Jakarta Sans', weight: 'bold' },
                        bodyFont: { family: 'Plus Jakarta Sans' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#94a3b8', stepSize: 1 },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    },
                    x: {
                        ticks: { color: '#94a3b8' },
                        grid: { display: false }
                    }
                }
            }
        });

    } catch (error) {
        console.error('Failed to initialize charts:', error);
    }
}
