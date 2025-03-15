function loginWithGoogle() {
    const clientId = "623565397438-56j4lk55qso3vcuosq10rpb4cosrv98n.apps.googleusercontent.com";
    const redirectUri = "http://localhost:8000/auth/callback"; // Your backend URL
    const scope = "email profile";
    const authUrl = `https://accounts.google.com/o/oauth2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=${scope}`;
    
    window.location.href = authUrl;
}