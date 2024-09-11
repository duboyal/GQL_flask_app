// src/Posts.js
import React, { useEffect, useState } from 'react';

function Posts() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Fetch data from the backend
        fetch('http://localhost:8000/scrape-craigslist')
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    setPosts(data.posts_list);
                } else {
                    setError('Failed to fetch posts');
                }
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            {posts.map((post) => (
                <div key={post.url} className="post-tile">
                    <h2>{post.title}</h2>
                    <p>{post.description}</p>
                    <a href={post.url} target="_blank" rel="noopener noreferrer">Read more</a>
                    <p>Created at: {new Date(post.created_at).toLocaleString()}</p>
                </div>
            ))}
        </div>
    );
}

export default Posts;
