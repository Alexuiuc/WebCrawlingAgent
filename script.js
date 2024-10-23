// script.js
async function sendToBackend() {
    const prompt = document.getElementById('prompt-input').value;
    const website = document.getElementById('website-input').value;
    const model = document.getElementById('model-selection').value;
    
    try {
      const response = await fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt, website: website, model: model }),  // Send prompt, website, and model selection
      });
  
      const result = await response.json();
      document.getElementById('output').textContent = result.result;  // Display result in the HTML
    } catch (error) {
      document.getElementById('output').textContent = 'Error: ' + error;
    }
  }
  