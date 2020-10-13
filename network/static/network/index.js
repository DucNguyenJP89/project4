
document.addEventListener('DOMContentLoaded', function() {
    // Clear out field 
    document.querySelector('#compose-content').value = '';

    // Add event when submit form
    document.querySelector('#compose-form').addEventListener('submit', function (event) {

        // Prevent default event
        event.preventDefault();

        // Get information from form input
        const content = document.querySelector('#compose-content').value;

        // Add post
        fetch('compose', {
            method: 'POST', body: JSON.stringify({
                content: content
            })
        })
            .then(response => {
                if (response.status !== 201) {
                    alert("Error: Cannot finish the request.");
                    console.log("Something wrong!");
                } else if (response.status === 201) {
                    alert("Success: Post added.");
                    console.log("Success");
                }
            });

        document.querySelector('#compose-content').value = '';


    })
})