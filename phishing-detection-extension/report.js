document.getElementById('generateReport').addEventListener('click', () => {
    // Simulate report generation (replace with real logic)
    const reportOutput = document.getElementById('reportOutput');
    reportOutput.innerHTML = `
      <h3>Phishing Detection Report</h3>
      <p>Total Attempts: 10</p>
      <p>Phishing Detected: 7</p>
      <p>Safe URLs: 3</p>
    `;
  });
  
  // Logout functionality
  document.getElementById('logout').addEventListener('click', () => {
    window.location.href = 'login.html';
  });