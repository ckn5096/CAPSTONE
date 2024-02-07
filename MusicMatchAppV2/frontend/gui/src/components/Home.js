// Home.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const Home = () => {
    const [message, setMessage] = useState('');
    const { authToken } = useAuth();

    useEffect(() => {
        console.log('Auth Token:', authToken);
        // Fetch data from the backend when the component mounts
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/home/', {
                    headers: {
                        Authorization: `Bearer ${authToken}`,
                    },
                });

                setMessage(response.data.message);
            } catch (error) {
                console.error('Error fetching data:', error.response.data);
            }
        };

        fetchData();
    }, [authToken]);

    return (
        <div>
            <h1>{message}</h1>
            {/* Add other stuff here for welcome */}
        </div>
    );
};

export default Home;