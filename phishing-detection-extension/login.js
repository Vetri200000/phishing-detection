document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    // Simulate authentication (replace with real auth logic)
    if (username === 'admin' && password === 'password') {
      window.location.href = 'dashboard.html'; // Redirect to dashboard
    } else {
      document.getElementById('error').innerText = 'Invalid credentials';
    }
  });