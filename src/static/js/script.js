document.addEventListener('DOMContentLoaded', function() {
    // ==========================================
    // 1. Dark Mode System Integration
    // ==========================================
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    if (prefersDarkScheme.matches) {
        document.body.classList.add('dark-mode');
    }
    prefersDarkScheme.addEventListener('change', e => {
        if (e.matches) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    });

    // ==========================================
    // 2. Custom Tooltip for Features
    // ==========================================
    const createTooltip = () => {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        document.body.appendChild(tooltip);
        return tooltip;
    };
    const tooltip = createTooltip();
    const featureCards = document.querySelectorAll('.card.h-100');
    
    featureCards.forEach(card => {
        card.addEventListener('mouseover', function(e) {
            const rect = this.getBoundingClientRect();
            const title = this.querySelector('h4').textContent;
            
            tooltip.textContent = `Explore details for ${title}`;
            tooltip.style.top = `${rect.bottom + window.scrollY}px`;
            tooltip.style.left = `${rect.left + window.scrollX + rect.width / 2 - tooltip.offsetWidth / 2}px`;
            tooltip.style.display = 'block';
        });
        
        card.addEventListener('mouseout', function() {
            tooltip.style.display = 'none';
        });
    });

    // ==========================================
    // 3. Scroll Animations
    // ==========================================
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
    window.addEventListener('load', animateOnScroll);
    window.addEventListener('scroll', animateOnScroll);
    // Initial run to capture elements already in viewport
    setTimeout(animateOnScroll, 100);

    // ==========================================
    // 4. Cascading Dropdowns Logic
    // ==========================================
    const stateSelect = document.getElementById('state');
    const districtSelect = document.getElementById('district');
    const marketSelect = document.getElementById('market');
    const commoditySelect = document.getElementById('commodity');
    const varietySelect = document.getElementById('variety');
    const gradeSelect = document.getElementById('grade');
    const predictionForm = document.getElementById('prediction-form');
    const loader = document.getElementById('loader');
    const resultCard = document.getElementById('result-card');

    stateSelect.addEventListener('change', function() {
        resetSelect(districtSelect, 'Select District');
        resetSelect(marketSelect, 'Select Market');
        if (this.value) {
            fetchDistricts(this.value);
        }
    });
    
    districtSelect.addEventListener('change', function() {
        resetSelect(marketSelect, 'Select Market');
        if (this.value) {
            fetchMarkets(this.value);
        }
    });
    
    commoditySelect.addEventListener('change', function() {
        resetSelect(varietySelect, 'Select Variety');
        resetSelect(gradeSelect, 'Select Grade');
        if (this.value) {
            fetchVarieties(this.value);
        }
    });
    
    varietySelect.addEventListener('change', function() {
        resetSelect(gradeSelect, 'Select Grade');
        if (this.value) {
            fetchGrades(this.value);
        }
    });

    function resetSelect(selectElement, defaultText) {
        selectElement.innerHTML = `<option value="" selected disabled>${defaultText}</option>`;
        selectElement.disabled = true;
    }
    
    function fetchDistricts(state) {
        fetch('/get_districts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ state: state })
        })
        .then(response => response.json())
        .then(districts => {
            populateSelect(districtSelect, districts, 'Select District');
            districtSelect.disabled = false;
        })
        .catch(error => console.error('Error fetching districts:', error));
    }
    
    function fetchMarkets(district) {
        fetch('/get_markets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ district: district })
        })
        .then(response => response.json())
        .then(markets => {
            populateSelect(marketSelect, markets, 'Select Market');
            marketSelect.disabled = false;
        })
        .catch(error => console.error('Error fetching markets:', error));
    }
    
    function fetchVarieties(commodity) {
        fetch('/get_varieties', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ commodity: commodity })
        })
        .then(response => response.json())
        .then(varieties => {
            populateSelect(varietySelect, varieties, 'Select Variety');
            varietySelect.disabled = false;
        })
        .catch(error => console.error('Error fetching varieties:', error));
    }
    
    function fetchGrades(variety) {
        fetch('/get_grades', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ variety: variety })
        })
        .then(response => response.json())
        .then(grades => {
            populateSelect(gradeSelect, grades, 'Select Grade');
            gradeSelect.disabled = false;
        })
        .catch(error => console.error('Error fetching grades:', error));
    }
    
    function populateSelect(selectElement, options, defaultText) {
        selectElement.innerHTML = `<option value="" disabled selected>${defaultText}</option>`;
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            selectElement.appendChild(optionElement);
        });
        if (options.length > 0) {
            selectElement.selectedIndex = 1;
            selectElement.dispatchEvent(new Event('change'));
        }
    }

    // ==========================================
    // 5. Prediction Form Submission Handler
    // ==========================================
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            loader.style.display = 'block';
            resultCard.style.display = 'none';
            
            const requestData = {
                state: stateSelect.value,
                district: districtSelect.value,
                market: marketSelect.value,
                commodity: commoditySelect.value,
                variety: varietySelect.value,
                grade: gradeSelect.value
            };
            
            fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            })
            .then(response => response.json())
            .then(data => {
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
                    
                    // Create or update price trend chart (Yesterday, Today, Tomorrow)
                    const trendDates = [data.yesterday_date, data.today_date, data.tomorrow_date];
                    const trendPrices = [data.yesterday_price, data.today_price, data.tomorrow_price];
                    createPriceHistoryChart(trendDates, trendPrices);
                    
                    // Smooth scroll to results
                    setTimeout(() => {
                        resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 100);
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
    
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }

    // ==========================================
    // 6. Chart.js Management (Canvas Reconstruction)
    // ==========================================
    let priceHistoryChart = null;
    let chartInitialized = false;
    
    function createPriceHistoryChart(dates, prices) {
        const canvas = document.getElementById('price-history-chart');
        if (!canvas) return;
        
        // Thoroughly destroy the existing chart if it exists to avoid canvas reuse warning
        if (chartInitialized || priceHistoryChart) {
            if (priceHistoryChart) {
                priceHistoryChart.destroy();
                priceHistoryChart = null;
            }
            
            // Re-create the canvas element to prevent internal canvas reference errors
            const newCanvas = document.createElement('canvas');
            newCanvas.id = 'price-history-chart';
            canvas.parentNode.replaceChild(newCanvas, canvas);
        }
        
        const ctx = document.getElementById('price-history-chart').getContext('2d');
        const formattedDates = dates.map(date => {
            const d = new Date(date);
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });
        
        // Setup Chart
        const isDark = document.body.classList.contains('dark-mode');
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
        const textColor = isDark ? '#e0e0e0' : '#666';

        priceHistoryChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: formattedDates,
                datasets: [{
                    label: 'Predicted Modal Price Trend',
                    data: prices,
                    backgroundColor: 'rgba(76, 175, 80, 0.15)',
                    borderColor: 'rgba(76, 175, 80, 1)',
                    borderWidth: 2.5,
                    pointBackgroundColor: 'rgba(76, 175, 80, 1)',
                    pointBorderColor: '#fff',
                    pointRadius: 4,
                    tension: 0.25
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: { color: gridColor },
                        ticks: { color: textColor },
                        title: {
                            display: true,
                            text: 'Price (₹)',
                            color: textColor
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: textColor },
                        title: {
                            display: true,
                            text: 'Arrival Date',
                            color: textColor
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: { color: textColor }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.85)',
                        titleFont: { size: 14 },
                        bodyFont: { size: 13 },
                        callbacks: {
                            label: function(context) {
                                return `Price: ₹${context.raw}`;
                            }
                        }
                    }
                }
            }
        });
        
        chartInitialized = true;
    }
});
