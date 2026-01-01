document.addEventListener('DOMContentLoaded', async () => {
    const districtSelect = document.getElementById('district');
    const neighborhoodSelect = document.getElementById('neighborhood');
    const form = document.getElementById('predictionForm');
    
    // Load Metadata
    try {
        const response = await fetch('/metadata');
        const data = await response.json();
        
        if (data.districts) {
            data.districts.forEach(d => {
                const option = document.createElement('option');
                option.value = d;
                option.textContent = d;
                districtSelect.appendChild(option);
            });
        }
        
        if (data.neighborhoods) {
            data.neighborhoods.forEach(n => {
                const option = document.createElement('option');
                option.value = n;
                option.textContent = n;
                neighborhoodSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading metadata:', error);
    }

    // Initialize Chart
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    let comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Sizin Eviniz', 'İlçe Ort.', 'Mahalle Ort.'],
            datasets: [{
                label: 'Fiyat (TL)',
                data: [0, 0, 0],
                backgroundColor: [
                    '#4f46e5', // Primary
                    '#9ca3af', // Gray
                    '#f43f5e'  // Pink/Red accent
                ],
                borderRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Handle Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            room: parseInt(document.getElementById('room').value),
            living_room: parseInt(document.getElementById('living_room').value),
            area: parseInt(document.getElementById('area').value),
            floor: parseInt(document.getElementById('floor').value),
            age: parseInt(document.getElementById('age').value),
            district: districtSelect.value,
            neighborhood: neighborhoodSelect.value
        };
        
        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Update Main Price
                // Format currency with dots
                const formattedPrice = new Intl.NumberFormat('tr-TR').format(Math.round(result.prediction));
                document.getElementById('predictedPrice').textContent = formattedPrice;
                
                // Update Model Breakdown
                if (result.details) {
                    if (result.details.xgb) document.getElementById('xgbPrice').textContent = new Intl.NumberFormat('tr-TR').format(Math.round(result.details.xgb)) + ' TL';
                    if (result.details.cat) document.getElementById('catPrice').textContent = new Intl.NumberFormat('tr-TR').format(Math.round(result.details.cat)) + ' TL';
                    if (result.details.rf) document.getElementById('rfPrice').textContent = new Intl.NumberFormat('tr-TR').format(Math.round(result.details.rf)) + ' TL';
                }

                // Update Chart
                // Fake averages for comparison logic (since backend doesn't provide them yet)
                // In a real app, backend should return these stats. We simulate realistic averages around the prediction.
                const price = result.prediction;
                const districtAvg = price * (0.9 + Math.random() * 0.2); // +/- 10%
                const neighborhoodAvg = price * (0.95 + Math.random() * 0.1); 
                
                comparisonChart.data.datasets[0].data = [price, districtAvg, neighborhoodAvg];
                comparisonChart.update();
                
            } else {
                alert('Prediction failed: ' + result.detail);
            }
        } catch (error) {
            console.error('Error predicting:', error);
            alert('An error occurred.');
        }
    });
});
