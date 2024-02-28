// // Home.js
// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import { useAuth } from './AuthContext';
//
// const Home = () => {
//     const [message, setMessage] = useState('');
//     const { authToken } = useAuth();
//
//     useEffect(() => {
//         console.log('Auth Token:', authToken);
//         // Fetch data from the backend when the component mounts
//         const fetchData = async () => {
//             try {
//                 const response = await axios.get('http://127.0.0.1:8000/home/', {
//                     headers: {
//                         Authorization: `Bearer ${authToken}`,
//                     },
//                 });
//
//                 setMessage(response.data.message);
//             } catch (error) {
//                 console.error('Error fetching data:', error.response.data);
//             }
//         };
//
//         fetchData();
//     }, [authToken]);
//
//     return (
//         <div>
//             <h1>{message}</h1>
//             {/* Add other stuff here for welcome */}
//         </div>
//     );
// };
//
// export default Home;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';


const Home = () => {
    const [message, setMessage] = useState('');
    const { authToken , storedToken,  logout } = useAuth();
    const navigate = useNavigate();

    const handleSignOut = () => {
        // Access the logout function from useAuth hook
        logout();

        navigate('/', {replace: true});
    };

    const goToProfileUpdate = () => {
        navigate('/profile/update'); // Navigate to the profile update page
    };

    const goToMusicPreferences = () => {
        navigate('/MusicPreference'); // Navigate to the music preferences page
    };

    // useEffect(() => {
    //     console.log('Auth Token:', authToken);
    //     // Fetch data from the backend when the component mounts
    //     const fetchData = async () => {
    //         try {
    //             const response = await axios.get('http://127.0.0.1:8000/home/', {
    //                 headers: {
    //                     Authorization: `Bearer ${authToken}`,
    //                 },
    //             });
    //
    //             setMessage(response.data.message);
    //         } catch (error) {
    //             console.error('Error fetching data:', error.response.data);
    //         }
    //     };
    //
    //     fetchData();
    // }, [authToken]);

     useEffect(() => {
        const fetchUserData = async () => {
            try {

                if (authToken) {
                    const response = await axios.get('http://127.0.0.1:8000/home/', {
                        headers: {
                            Authorization: `Bearer ${authToken}`,
                        },
                    });
                    setMessage(response.data.message);
                }

                if (storedToken) {
                    const response = await axios.get('http://127.0.0.1:8000/home/', {
                        headers: {
                            Authorization: `Bearer ${storedToken}`,
                        },
                    });
                    setMessage(response.data.message);
                }

            } catch (error) {
                console.error('Error fetching data!!:', error.response.data);
               navigate('/login', { replace: true }); // Redirect to login page if authentication fails
            }
        };

        if (authToken || storedToken) {
            fetchUserData();
            console.log('Auth token after login ' , authToken);
        }

        else{
           // console.log('Error fetching auth token');
            console.log('Error fetching auth token' , authToken);
           navigate('/login', { replace: true }); // Redirect to login page if authToken is not available
        }
    }, [authToken, storedToken,  navigate]);

    return (
        <div>
            <h1>{message}</h1>
            {/* Add other stuff here for welcome */}
            <button onClick={goToProfileUpdate}>Go to Profile Update</button> {/* Button to navigate to the profile update page */}

            <button onClick={goToMusicPreferences}>Go to Music Preferences</button>

            {/* Add sign-out button */}
            <button onClick={handleSignOut}>Sign Out</button>
        </div>
    );
};

export default Home;

