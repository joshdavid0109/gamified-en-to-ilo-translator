const form = document.getElementById('login-form');

  form.addEventListener('submit', async (event) => {
    handleLogin();
});

async function handleLogin(){
    event.preventDefault();

    const username = document.getElementById('UsernameInput').value;
    const password = document.getElementById('PasswordInput').value;

    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password
    }),
});

    const data = await response.json();

    if (data.success) {
      window.location.href = '/mainpage';
    } else {
      alert(data.error);
    }
}