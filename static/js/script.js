// Function to show and then hide the message with a fade-out effect
function showMessage() {
    const message = document.getElementById('message');
    message.classList.remove('fade-out-hidden'); // Make it visible
    setTimeout(() => {
        message.classList.add('fade-out-hidden'); // Start fade-out after 1 second
    }, 1000); // Show for 1 second before fading out
}

// Call the function to display the message
showMessage();

