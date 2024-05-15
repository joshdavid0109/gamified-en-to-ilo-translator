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

// Define a function to update the HTML content with the fetched data
async function updateContent() {

    // Clear all event listeners
    const buttons = document.querySelectorAll('.ripple-effect');
    buttons.forEach(button => {
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
    });

    const data = await fetchData();

    if (data) {
        // Update word
        const wordElement = document.querySelector('h1[data-aos="fade-right"]');
        wordElement.textContent = data.word.trim(); // Trim any leading/trailing whitespace

        // Update choices
        const buttons = document.querySelectorAll('.ripple-effect');
        buttons.forEach((button, index) => {
            button.textContent = data.choices[index];
            // Add event listener to check correctness
            button.addEventListener('click', () => {
                if (button.textContent === data.correct_answer) {
                    // Correct answer
                    const modal = new bootstrap.Modal(document.getElementById('correctModal'));
                    modal.show();
                    setToLoading()
                    updateContent()
                } else {
                    const modal = new bootstrap.Modal(document.getElementById('wrongModal'));
                    modal.show();
                    setToLoading()
                    updateContent()
                }
            });
        });
    }
}

function setToLoading() {
    // Set buttons' text content to "loading..."
    const buttons = document.querySelectorAll('.ripple-effect');
    buttons.forEach(button => {
        button.textContent = 'loading...';
    });

    // Set word and round text content to "loading..."
    const wordElement = document.querySelector('h1[data-aos="fade-right"]');
    wordElement.textContent = 'loading...';

    const roundElement = document.querySelector('p[data-aos="fade-right"]');
    roundElement.textContent = 'round: loading...';
}


// Call the updateContent function initially
updateContent();
