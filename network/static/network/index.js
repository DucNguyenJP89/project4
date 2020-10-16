document.addEventListener('DOMContentLoaded', function() {
    
    // Load all posts view when click the link
    document.querySelector('#all').addEventListener('click', function(event) {
        event.preventDefault();
        load_posts('all');
        return false;
    })

    // Check if there is following-view link
    if (document.querySelector('#following')) {
        // load following-view when click
        document.querySelector('#following').addEventListener('click', (event) => {
            event.preventDefault();
            // Load following-view
            load_posts('following');
            return false;
        })

    };

    // Check if there is compose view
    if (document.querySelector('#compose-post')) {
        // Clear out field 
        document.querySelector('#compose-content').value = '';

        // Add event when submit form
        document.querySelector('#compose-form').addEventListener('submit', function(event) {

            // Prevent default event
            event.preventDefault();

            // Get information from form input
            const content = document.querySelector('#compose-content').value;

            // Add post
            fetch('posts/compose', {
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
                    return load_posts('all');
                }
            });

            document.querySelector('#compose-content').value = '';


        })
    };

    // Load all posts by default
    load_posts('all');

})

function load_posts(postview) {

    // Clear the view before loading new view
    document.querySelector('#posts-view').innerHTML = '';

    // Get posts and add posts to post view
    fetch(`posts/${postview}`)
    .then(response => response.json())
    .then(posts => {
        if (posts.length === 0) {

            // Create view with 0 post message
            const noPost = document.createElement('div');
            noPost.className = 'no-post';
            noPost.innerHTML = `You haven't followed anyone yet.`;

            // Add to view
            document.querySelector('#posts-view').append(noPost);
        } else {
            posts.forEach(add_post);
        }
    })

    // Hide form if it is not "all" view
    if (`${postview}` !== 'all') {
        document.querySelector('#compose-post').style.display = 'none';
    } else {
        document.querySelector('#compose-post').style.display = 'block';
    }
    // Show the view name
    document.querySelector('#post-view-head').innerHTML = `<h3 class='m-2 p-2'>${postview.charAt(0).toUpperCase() + postview.slice(1)} Posts</h3>`;  

};

function add_post(post) {

    // Create new post with poster, content, timestamp
    const newPost = document.createElement('div');
    newPost.className = 'border rounded m-2 px-2 pt-2';

    const newPoster = document.createElement('h5');
    newPoster.innerHTML = `${post.poster}`;
    newPost.appendChild(newPoster);

    // Get logged in user
    if (document.querySelector('#login-user')) {
        const loginUser = document.querySelector('#login-user').innerText;
        if (post.poster === loginUser) {
            const linkEdit = document.createElement('div');
            linkEdit.innerHTML = `<a href='#' id="edit-post">Edit</a>`;
            newPost.appendChild(linkEdit);
        }
    };

    const newContent = document.createElement('p');
    newContent.innerHTML = `${post.content}`;

    const newTimeStamp = document.createElement('p');
    newTimeStamp.className = 'time-stamp';
    newTimeStamp.innerHTML = `${post.timestamp}`;

    const newFavorites = document.createElement('div');
    newFavorites.className = 'liked';
    const numOfLikes = post.liked.length;
    newFavorites.innerHTML = `${numOfLikes} likes`;

    
    
    newPost.appendChild(newContent);
    newPost.appendChild(newFavorites);
    newPost.appendChild(newTimeStamp);

    // Add new post to post view
    document.querySelector('#posts-view').append(newPost);

}