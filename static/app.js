// app.js
document.getElementById('sepsisForm').addEventListener('submit', async function(e) {
    e.preventDefault();
  
    const heartRate = parseFloat(document.getElementById('heartRate').value);
    const respRate = parseFloat(document.getElementById('respRate').value);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const wbc = parseFloat(document.getElementById('wbc').value);
    const lactate = parseFloat(document.getElementById('lactate').value);
  
    const data = {
      HeartRate: heartRate,
      RespRate: respRate,
      Temp: temperature,
      WBC: wbc,
      Lactate: lactate
    };
  
    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      const result = await response.json();
  
      if (result.sepsis_risk !== undefined) {
        document.getElementById('result').innerText = `Sepsis Risk: ${result.sepsis_risk}`;
      } else {
        document.getElementById('result').innerText = `Error: ${result.error || 'Unknown error'}`;
      }
    } catch (error) {
      document.getElementById('result').innerText = 'Error connecting to the server.';
      console.error('Error:', error);
    }
  });
  