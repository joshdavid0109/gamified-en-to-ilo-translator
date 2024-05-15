
//selected_translation - target
export function submitanswer(selected_translation, isCorrect){
    fetch('http://127.0.0.1:5000/submitanswer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            selected_translation: selected_translation,
            isCorrect: isCorrect
        }),
        })
        .then(response => response.json())
        .then(data => console.log('Result:', data.result))
        .catch((error) => console.error('Error:', error));
}