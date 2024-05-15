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
    const data = await fetchData();

    if (data) {
        // Update word
        const wordElement = document.querySelector('h1[data-aos="fade-right"]');
        wordElement.textContent = data.word.trim(); // Trim any leading/trailing whitespace

        // Update choices
        const buttons = document.querySelectorAll('.ripple-effect');
        buttons.forEach((button, index) => {
            button.textContent = data.choices[index];
        });
    }
}

// Call the updateContent function initially
updateContent();
