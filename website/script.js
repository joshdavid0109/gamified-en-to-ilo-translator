
function selectOption(option) {

    // Remove the selected class from all options
    var options = document.getElementsByClassName('option');
    for (var i = 0; i < options.length; i++) {
      options[i].classList.remove('selected');
    }
  
    // Add the selected class to the clicked option
    option.classList.add('selected');
}

$(document).ready(function() {
    $.ajax({
        url: 'http://127.0.0.1:5500',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            // Update the content of the randomWord div with the received random word
            console.log(response.random_word)

            console.log($('#word-to-translate').val());
        },
        error: function(xhr, status, error) {
            // Handle error if the request fails
            console.error('Error fetching random word:', error);
        }
    });

    $("#submit").on("click", function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Define the data to send in the POST request
        const postData = {
            text: $('#answer').val(),
            target_language: 'ilo'
        };

        // Send a POST request to the /translate endpoint
        fetch("http://127.0.0.1:5000/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json" // Specify content type as JSON
            },
            body: JSON.stringify(postData) // Convert postData to JSON format
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json(); // Parse the JSON response
        })
        .then(data => {
            console.log(data)
            // Display the translated text in the output div
            // $("#word-to-translate").text(data.random_word);
            // $("#output").text(data.translated_text);
        })
        .catch(error => {
            console.error("Error translating text:", error);
        });
    });
});



// $(document).ready(function() {
//     $("#submit").on("click", function(event) {

//         event.preventDefault(); // Prevent the default form submission behavior

//         // Define the data to send in the POST request
//         const postData = {
//             answer: $('#answer').val(),
//         };

//         // Create an array to hold the promises for the GET and POST requests
//         const promises = [];

//         // Send a GET request to the /users endpoint
//         const getUsersPromise = fetch("http://127.0.0.1:5000/users", {
//             method: "GET",
//             headers: {
//                 "Content-Type": "application/json" // Specify that we're sending JSON data
//             }
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error("Network response was not ok");
//             }
//             return response.json(); // Parse the JSON response
//         })
//         .then(data => {
//             // Display the data in the output div
//             $("#output").text(JSON.stringify(data));
//         })
//         .catch(error => {
//             console.error("Error fetching data:", error);
//         });

//         // Add the GET request promise to the promises array
//         promises.push(getUsersPromise);

//         // Send a POST request to the /users endpoint
//         const postUsersPromise = $.ajax({
//             url: 'http://127.0.0.1:5000/users',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify(postData)
//         });

//         // Add the POST request promise to the promises array
//         promises.push(postUsersPromise);

//         // Execute both promises concurrently
//         Promise.all(promises)
//             .then(results => {
//                 console.log('Both requests completed successfully');
//                 console.log('GET request result:', results[0]);
//                 console.log('POST request result:', results[1]);
//             })
//             .catch(error => {
//                 console.error('Error executing promises:', error);
//             });
//     });
// });
