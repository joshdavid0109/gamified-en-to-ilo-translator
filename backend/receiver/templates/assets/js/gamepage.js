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

                console.log("an answer is clicked")
                

                if (button.textContent === data.correct_answer) {

                    console.log("CORRECT ANSWER IS CLICKED?: " +data.correct_answer)
                    getUserId()
                    .then(userid => {
                        console.log("My user ID is:", userid);
                        const postData = {
                            selectedTranslation: data.correct_answer,
                            isCorrect: "true",
                            userId: userid
                        };
                        submitAnswer(postData).then(responseData => {
                            if (responseData) {
                                console.log("Response data:", responseData);
                                console.log("Points:", responseData.points);
                                console.log("Score:", responseData.score);
                                console.log("Tier:", responseData.tier);

                                const modalBody = document.querySelector('#correctModal .modal-body p');
                                modalBody.textContent = `Correct! You gained ${responseData.score} points.`;

                                const pointz = document.getElementById("points");
                                pointz.innerHTML = "Points: "+responseData.points + " [" +responseData.tier+"] "

                                const modal = new bootstrap.Modal(document.getElementById('correctModal'));
                                modal.show();
                            }
                        });
                    });

                    
                    
                    setToLoading()
                    updateContent()
                } else {
                    getUserId()
                    .then(userid => {
                        console.log("My user ID is:", userid);
                        const postData = {
                            selectedTranslation: data.correct_answer,
                            isCorrect: "false",
                            userId: userid
                        };
                        submitAnswer(postData).then(responseData => {
                            if (responseData) {
                                console.log("Response data:", responseData);
                                console.log("Points:", responseData.points);
                                console.log("Score:", responseData.score);
                                console.log("Tier:", responseData.tier);

                                const modalBody = document.querySelector('#wrongModal .modal-body p');
                                modalBody.textContent = `Wrong! You lost ${responseData.score} points.`;

                                const pointz = document.getElementById("points");
                                pointz.innerHTML = "Points: "+responseData.points + " [" +responseData.tier+"] "

                                const modal = new bootstrap.Modal(document.getElementById('wrongModal'));
                                modal.show();
                            }
                        });
                    });
                    
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
}


// Call the updateContent function initially
updateContent();

async function getUserId(){
    try {
        const response = await fetch('http://127.0.0.1:5000/getuserid');
        const data = await response.json();
        return data.userid;
    } catch (error) {
        console.error('Error fetching user ID:', error);
        return null;
    }
}

async function getPoints(){
    try {
        const response = await fetch('http://127.0.0.1:5000/getpoints');
        const data = await response.json();
        return data.points;
    } catch (error) {
        console.error('Error fetching points:', error);
        return null;
    }
}

async function submitAnswer(data) {
    try {
        const response = await fetch('http://127.0.0.1:5000/submitanswer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const responseData = await response.json();
        console.log('Submission response:', responseData);
        return responseData
  
    } catch (error) {
        console.error('Error submitting answer:', error);
    }
}