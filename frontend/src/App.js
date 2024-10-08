import React, { useState, useEffect } from 'react';
import './styles/App.css'; // Correct path to the CSS file

function App() {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/scrape-daya')
            .then((response) => response.json())
            .then((data) => {
                console.log('Received data:', data);  // This will show the entire response
                // Access the posts inside the 'data.data' field
                if (data && Array.isArray(data.data)) {
                    setPosts(data.data);  // Access the 'data' field to get the posts
                } else {
                    console.error('Invalid data format:', data);
                    setPosts([]); // Default to an empty array if data is invalid
                }
            })
            .catch((error) => console.error('Error fetching posts:', error));
    }, []);


    return (
        <div>
            <h1>Craigslist Posts</h1>
            <div className="post-grid">
                {posts.length > 0 ? (
                    posts.map((post, index) => (
                        <div className="post-tile" key={index}>
                            <div className="post-title">{post.title}</div>
                            <div className="post-description">{post.description}</div>
                            <a
                                href={post.url}
                                className="post-link"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                Read more
                            </a>
                            <div className="post-date">
                                Created at: {new Date(post.created_at).toLocaleString()}
                            </div>
                        </div>
                    ))
                ) : (
                    <p>No posts available.</p> // Fallback message if there are no posts
                )}
            </div>
        </div>
    );
}

export default App;




// import React, { useState, useEffect } from 'react';
// import './styles/App.css'; // Correct path to the CSS file

// function App() {
//     const [posts, setPosts] = useState([]);

//     useEffect(() => {
//         fetch('http://localhost:8000/scrape-daya')// ('http://localhost:8000/scrape-craigslist') or daya
//             .then((response) => response.json())
//             .then((data) => setPosts(data.posts_list))
//             .catch((error) => console.error('Error fetching posts:', error));
//     }, []);

//     return (
//         <div>
//             <h1>Craigslist Posts</h1>
//             <div className="post-grid">
//                 {posts.map((post, index) => (
//                     <div className="post-tile" key={index}>
//                         <div className="post-title">{post.title}</div>
//                         <div className="post-description">{post.description}</div>
//                         <a
//                             href={post.url}
//                             className="post-link"
//                             target="_blank"
//                             rel="noopener noreferrer"
//                         >
//                             Read more
//                         </a>
//                         <div className="post-date">
//                             Created at: {new Date(post.created_at).toLocaleString()}
//                         </div>
//                     </div>
//                 ))}
//             </div>
//         </div>
//     );
// }

// export default App;
