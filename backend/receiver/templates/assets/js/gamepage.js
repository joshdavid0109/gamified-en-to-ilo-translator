// Define a function to fetch data from the API
async function fetchData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/get_choices', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        const data = await response.json();
        console.log(data)
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to handle correct answer modal
function handleCorrectAnswerModal(isCorrect) {
    // Show alert indicating correctness
    if (isCorrect) {
        alert('Congratulations! Your answer is correct.');
    } else {
        alert('Oops! Your answer is incorrect.');
    }

    // Set all buttons back to loading state
    const buttons = document.querySelectorAll('.ripple-effect');
    buttons.forEach(button => {
        button.textContent = 'loading...';
    });

    // Execute updateContent
    updateContent();
}

// Define a function to update the HTML content with the fetched data
async function updateContent() {
    const data = await fetchData();

    if (data) {
        // Update word
        const wordElement = document.querySelector('h1[data-aos="fade-right"]');
        wordElement.textContent = data.word.trim(); // Trim any leading/trailing whitespace

        // Update choices
        const buttons = document.querySelectorAll('.ripple-effect');
        buttons.forEach((button, index) => {
            // Remove existing event listener
            button.removeEventListener('click', handleClick);

            button.textContent = data.choices[index];
            // Add event listener to check correctness
            button.addEventListener('click', handleClick);
        });

        // Function to handle button click
        function handleClick() {
            if (this.textContent === data.correct_answer) {
                // Correct answer
                handleCorrectAnswerModal(true);
            } else {
                // Incorrect answer
                handleCorrectAnswerModal(false);
            }
        }
    }
}

updateContent()