$(document).ready(function() {
    // Function to handle option selection
    function selectOption(option) {
        $('.option').removeClass('selected'); 
        $(option).addClass('selected'); 
    }

    // Function to fetch a word and its translations from the server
    function fetchWord(difficulty, callback) {
        $.ajax({
            url: "http://127.0.0.1:5000/" + difficulty,
            type: "GET",
            dataType: "json",
            success: function(data) {
                // Pass data to the callback function
                callback(data);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching random word:", error);
            }
        });
    }

    function updateWordAndChoices(data) {
        console.log("Random word:", data.word);

        $('#word-to-translate').text(data.word);

        $('#word-to-translate').data('correct-answer', data.correct_answer);

        // Populate the options with translations
        var options = $('.option');
        $.each(options, function(index, option) {
            $(option).text(data.choices[index]);
        });
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
    
        // Send the selected translation, correctness, and other data to the server for further processing
        $.ajax({
            url: '/submitanswer',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                selectedTranslation: selectedTranslation,
                isCorrect: isCorrect
            }),
            success: function(data) {
                console.log(data); // For debugging
                // Handle server response as needed
    
                // Update word and choices after submission
                fetchWord('medium', updateWordAndChoices); // Change 'easy' to appropriate difficulty
            },
            error: function(error) {
                console.error("Error:", error);
                // Handle errors
            }
        });
    
        // Show the pop-up message based on correctness
        if (isCorrect) {
            $('#correctModal').modal('show');
        } else {
            $('#incorrectModal').modal('show');
        }
    });
    

    // Fetch word for each difficulty level initially
    fetchWord('easy', updateWordAndChoices); // Change 'easy' 
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
