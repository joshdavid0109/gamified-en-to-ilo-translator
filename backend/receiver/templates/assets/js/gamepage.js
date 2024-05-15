async function fetchChoicesAndUpdateButtons() {
    try {
        const response = await fetch('/submitanswer'); // Change the URL to match your server route
        const data = await response.json();

        document.getElementById('question').innerText = data.word;

        const buttons = ['button1', 'button2', 'button3', 'button4'];
        data.choices.forEach((choice, index) => {
            document.getElementById(buttons[index]).innerText = choice;
        });
    } catch (error) {
        console.error('Error fetching choices:', error);
    }
}
