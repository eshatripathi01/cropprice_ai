// Additional JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Dark mode toggle functionality
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    if (prefersDarkScheme.matches) {
        document.body.classList.add('dark-mode');
    }
    
    // Price history chart variable
    let priceHistoryChart = null;
    
    // Track if chart has been initialized
    let chartInitialized = false;
    
    // Custom tooltip functionality
    const createTooltip = () => {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        document.body.appendChild(tooltip);
        return tooltip;
    };
    
    const tooltip = createTooltip();
    
    // Add tooltip to feature cards
    const featureCards = document.querySelectorAll('.card.h-100');
    
    featureCards.forEach(card => {
        card.addEventListener('mouseover', function(e) {
            const rect = this.getBoundingClientRect();
            const title = this.querySelector('h4').textContent;
            
            tooltip.textContent = `Learn more about ${title}`;
            tooltip.style.top = `${rect.bottom + window.scrollY}px`;
            tooltip.style.left = `${rect.left + window.scrollX + rect.width / 2 - tooltip.offsetWidth / 2}px`;
            tooltip.style.display = 'block';
        });
        
        card.addEventListener('mouseout', function() {
            tooltip.style.display = 'none';
        });
    });
    
    // Add animation classes to elements when they come into view
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.card, .feature-icon, h2, .result-card, .price-card');
        
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            
            // Check if element is in viewport
            if (elementTop < window.innerHeight && elementBottom > 0) {
                element.classList.add('fade-in');
            }
        });
    };
    
    // Run animation check on load and scroll
    window.addEventListener('load', animateOnScroll);
    window.addEventListener('scroll', animateOnScroll);
    
    // Form submission handler
    const predictionForm = document.getElementById('prediction-form');
    const loader = document.getElementById('loader');
    const resultCard = document.getElementById('result-card');
    
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loader
            loader.style.display = 'block';
            resultCard.style.display = 'none';
            
            // Get form data
            const state = document.getElementById('state').value;
            const district = document.getElementById('district').value;
            const market = document.getElementById('market').value;
            const commodity = document.getElementById('commodity').value;
            const variety = document.getElementById('variety').value;
            const grade = document.getElementById('grade').value;
            
            // Create request data
            const requestData = {
                state: state,
                district: district,
                market: market,
                commodity: commodity,
                variety: variety,
                grade: grade
            };
            
            // Send prediction request
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
            .then(response => response.json())
            .then(data => {
                // Hide loader
                loader.style.display = 'none';
                
                if (data.success) {
                    // Update price values
                    document.getElementById('yesterday-price').textContent = data.yesterday_price;
                    document.getElementById('today-price').textContent = data.today_price;
                    document.getElementById('tomorrow-price').textContent = data.tomorrow_price;
                    
                    // Update date labels
                    document.getElementById('yesterday-date').textContent = formatDate(data.yesterday_date);
                    document.getElementById('today-date').textContent = formatDate(data.today_date);
                    document.getElementById('tomorrow-date').textContent = formatDate(data.tomorrow_date);
                    
                    // Show result card
                    resultCard.style.display = 'block';
                    
                    // Create or update price history chart
                    createPriceHistoryChart(data.historical_dates, data.historical_prices);
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                loader.style.display = 'none';
                alert('Error: ' + error);
            });
        });
    }
    
    // Format date for display
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
    
    // Create or update price history chart
    function createPriceHistoryChart(dates, prices) {
        // Get the canvas element
        const canvas = document.getElementById('price-history-chart');
        
        // Thoroughly destroy the existing chart if it exists
        if (chartInitialized) {
            if (priceHistoryChart) {
                priceHistoryChart.destroy();
                priceHistoryChart = null;
            }
            
            // Create a new canvas element to replace the old one
            const newCanvas = document.createElement('canvas');
            newCanvas.id = 'price-history-chart';
            canvas.parentNode.replaceChild(newCanvas, canvas);
        }
        
        // Get the context from the new or existing canvas
        const ctx = document.getElementById('price-history-chart').getContext('2d');
        
        // Format dates for display
        const formattedDates = dates.map(date => {
            const d = new Date(date);
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        
        // Create new chart
        priceHistoryChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: formattedDates,
                datasets: [{
                    label: 'Historical Modal Prices',
                    data: prices,
                    backgroundColor: 'rgba(76, 175, 80, 0.2)',
                    borderColor: 'rgba(76, 175, 80, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(76, 175, 80, 1)',
                    pointBorderColor: '#fff',
                    pointRadius: 4,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Price (₹)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                return `Price: ₹${context.raw}`;
                            }
                        }
                    }
                }
            }
        });
        
        // Mark chart as initialized
        chartInitialized = true;
    }
});