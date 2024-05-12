$(document).ready(function() {
    // Function to handle option selection
    function selectOption(option) {
        $('.option').removeClass('selected'); // Remove selected class from all options
        $(option).addClass('selected'); // Add selected class to the clicked option
    }

    // Submit form event listener
    $('#quiz-form').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Retrieve the selected option
        var selectedOption = $('.option.selected');
        var selectedTranslation = selectedOption.text();

        // Retrieve the correct answer from the hidden input field
        var correctAnswer = $('#word-to-translate').data('correct-answer');

        // Check if the selected translation matches the correct answer
        var isCorrect = (selectedTranslation === correctAnswer);

        // Send the selected translation and correctness to the server for further processing
        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                selectedTranslation: selectedTranslation, 
                isCorrect: isCorrect 
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // For debugging
            // Handle server response as needed
        })
        .catch(error => {
            console.error("Error:", error);
            // Handle errors
        });

        // Show the pop-up message based on correctness
        if (isCorrect) {
            $('#correctModal').modal('show');
        } else {
            $('#incorrectModal').modal('show');
        }
    });

    // Fetch a random word and its translations from the server
    function fetchWord(difficulty) {
        $.ajax({
            url: "http://127.0.0.1:5000/" + difficulty,
            type: "GET",
            dataType: "json",
            success: function(data) {
                console.log("Random word:", data.word);
                // Display the random word on the page
                $('#word-to-translate').text(data.word);
                // Set the correct answer as a data attribute for later retrieval
                $('#word-to-translate').data('correct-answer', data.correct_answer);

                // Populate the options with translations
                var options = $('.option');
                $.each(options, function(index, option) {
                    $(option).text(data.choices[index]);
                });
            },
            error: function(xhr, status, error) {
                console.error("Error fetching random word:", error);
            }
        });
    }

    // Fetch word for each difficulty level
    fetchWord('easy');
    fetchWord('medium');
    fetchWord('hard');

    // Click event listener for option selection
    $('.option').click(function() {
        selectOption(this);
    });

    // Fetch user data
    $.ajax({
        url: "http://127.0.0.1:5000/user",
        type: "GET",
        dataType: "json",
        success: function(data) {
            console.log(data);
            $('#profile-name').text(data.username);
            $('#score').text(data.points);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching user data:", error);
        }
    });
});
