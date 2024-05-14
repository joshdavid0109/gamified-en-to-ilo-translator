const form = document.getElementById('login-form');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('UsernameInput').value;
    const password = document.getElementById('PasswordInput').value;
    console.log(username)

    const response = await fetch('http://127.0.0.1:5000/login', {
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
});

