document.addEventListener('DOMContentLoaded', function() {
    // Check exists and add event listener for following link
    if (document.querySelector('#following')) {

        //Add event listener when clicked
        document.querySelector('#following').addEventListener('click', function(event) {
            // Prevent default event
            event.preventDefault();

            load_posts('following');
        })

    }

    // Check if there is compose view
    if (document.querySelector('#compose-view')) {
        // Clear out field 
        document.querySelector('#compose-content').value = '';

        // Add event when submit form
        document.querySelector('#compose-form').addEventListener('submit', function (event) {

            // Prevent default event
            // event.preventDefault();

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
                        console.log("Success");
                    }
                });

            document.querySelector('#compose-content').value = '';


        })
    }

    // Load all posts by default
    load_posts('all');

})

function load_posts(postview) {

    // Get posts and add posts to post view
    fetch(`posts/${postview}`)
    .then(response => response.json())
    .then(posts => {
        if (posts.length === 0) {

            // Create view with 0 post message
            const noPost = document.createElement('div');
            noPost.className = 'no-post';
            noPost.innerHTML = 'No post yet.';

            // Add to view
            document.querySelector('#posts-view').append(noMail);
        } else {
            posts.forEach(add_post);
        }
    })

    // Hide form if it is not "all" view
    if (`${postview}` !== 'all') {
    document.querySelector('#compose-post').style.display = 'none';
    }

    // Show the mailbox name
    document.querySelector('#post-view-head').innerHTML = `<h3>${postview.charAt(0).toUpperCase() + postview.slice(1)} Posts</h3>`;  

};

function add_post(post) {

    // Create new post with poster, content, timestamp
    const newPost = document.createElement('div');

    const newPoster = document.createElement('h5');
    newPoster.innerHTML = `${post.poster}`;

    const newContent = document.createElement('p');
    newContent.innerHTML = `${post.content}`;

    const newTimeStamp = document.createElement('p');
    newTimeStamp.innerHTML = `${post.timestamp}`;

    newPost.appendChild(newPoster);
    newPost.appendChild(newContent);
    newPost.appendChild(newTimeStamp);

    // Add new post to post view
    document.querySelector('#posts-view').append(newPost);

}