document.getElementById('checkUrl').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const currentUrl = tabs[0].url;
      document.getElementById('result').innerText = "Checking...";
  
      // Send the URL to your ML model (local or server)
      fetch('http://localhost:5000/predict', {  // Replace with your model's API endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: currentUrl }),
      })
        .then((response) => response.json())
        .then((data) => {
          document.getElementById('result').innerText = `Result: ${data.result}`;
        })
        .catch((error) => {
          document.getElementById('result').innerText = "Error checking URL.";
        });
    });
  });