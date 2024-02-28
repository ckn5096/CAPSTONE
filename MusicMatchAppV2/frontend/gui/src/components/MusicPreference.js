// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import { useAuth } from './AuthContext';
// import { useNavigate } from 'react-router-dom';
//
// const apiUrl = 'http://127.0.0.1:8000/MusicPreference/'; // Base URL for your API
//
// const MusicPreferences = () => {
//     const { authToken, logout } = useAuth();
//     const [preferences, setPreferences] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);
//     const [recommendedSongs, setRecommendedSongs] = useState([]);
//     const navigate = useNavigate();
//     const [newPreference, setNewPreference] = useState({
//         favorite_genre: '',
//         favorite_artist: '',
//         favorite_song: ''
//     });
//
//     const handleSignOut = () => {
//         // Access the logout function from useAuth hook
//         logout();
//
//         navigate('/', { replace: true });
//     };
//
//     // Function to fetch preferences
//     const fetchPreferences = async () => {
//         try {
//             const response = await axios.get(apiUrl, {
//                 headers: {
//                     Authorization: `Bearer ${authToken}`,
//                 },
//             });
//             setPreferences(response.data);
//             setLoading(false);
//         } catch (error) {
//             setError(error.response.data);
//             setLoading(false);
//         }
//     };
//
//     useEffect(() => {
//         if (authToken) {
//             fetchPreferences();
//         }
//     }, [authToken]);
//
//     const handleSubmit = async (event) => {
//         event.preventDefault();
//         try {
//             await axios.post(apiUrl, newPreference, {
//                 headers: {
//                     Authorization: `Bearer ${authToken}`,
//                     'Content-Type': 'application/json',
//                 },
//             });
//
//             // Generate playlist
//             await axios.post('http://127.0.0.1:8000/generate_playlist/', newPreference, {
//                 headers: {
//                     Authorization: `Bearer ${authToken}`,
//                     'Content-Type': 'application/json',
//                 },
//             });
//
//             // Fetch recommended songs
//             const response = await axios.post('http://127.0.0.1:8000/generate_playlist/', newPreference, {
//                 headers: {
//                     Authorization: `Bearer ${authToken}`,
//                     'Content-Type': 'application/json',
//                 },
//             });
//             console.log('Recommended Songs Response:', response.data); // Debugging log
//             setRecommendedSongs(response.data);
//
//             // Refresh preferences after creating a new one
//             fetchPreferences();
//             setNewPreference({
//                 favorite_genre: '',
//                 favorite_artist: '',
//                 favorite_song: ''
//             });
//         } catch (error) {
//             setError(error.response.data);
//         }
//     };
//
//     const handleDeletePreference = async () => {
//         try {
//             await axios.delete(apiUrl, {
//                 headers: {
//                     Authorization: `Bearer ${authToken}`,
//                 },
//             });
//             // Refresh preferences after deleting
//             fetchPreferences();
//         } catch (error) {
//             setError(error.response.data);
//         }
//     };
//
//     const handleChange = (event) => {
//         const { name, value } = event.target;
//         setNewPreference({
//             ...newPreference,
//             [name]: value
//         });
//     };
//
//     return (
//         <div>
//             {loading && <p>Loading...</p>}
//             {error && <p>Error: {error}</p>}
//             {preferences && (
//                 <div>
//                     <h2>Your Music Preferences</h2>
//                     <ul>
//                         <li>Favorite Genre: {preferences.favorite_genre}</li>
//                         <li>Favorite Artist: {preferences.favorite_artist}</li>
//                         <li>Favorite Song: {preferences.favorite_song}</li>
//                     </ul>
//                     <button onClick={handleDeletePreference}>Delete Preferences</button>
//                 </div>
//             )}
//             {recommendedSongs.length > 0 && (
//                 <div>
//                     <h2>Recommended Songs</h2>
//                     <ul>
//                         {recommendedSongs.map((song, index) => (
//                             <li key={index}>{song.name} - {song.artist}</li>
//                         ))}
//                     </ul>
//                 </div>
//             )}
//             <h2>Create New Preferences</h2>
//             <form onSubmit={handleSubmit}>
//                 <input type="text" placeholder="Favorite Genre" name="favorite_genre" value={newPreference.favorite_genre} onChange={handleChange} />
//                 <input type="text" placeholder="Favorite Artist" name="favorite_artist" value={newPreference.favorite_artist} onChange={handleChange} />
//                 <input type="text" placeholder="Favorite Song" name="favorite_song" value={newPreference.favorite_song} onChange={handleChange} />
//                 <button type="submit">Save Preferences and Generate Playlist</button>
//             </form>
//
//             <button onClick={handleSignOut}>Sign Out</button>
//         </div>
//     );
// };
//
// export default MusicPreferences;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';

const apiUrl = 'http://127.0.0.1:8000/MusicPreference/'; // Base URL for your API
const playlistUrl = 'http://127.0.0.1:8000/UserPlaylist/'; // URL for fetching playlists

const MusicPreferences = () => {
    const { authToken, logout } = useAuth();
    const [preferences, setPreferences] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [recommendedSongs, setRecommendedSongs] = useState([]);
    const [userPlaylist, setUserPlaylist] = useState(null); // State to store user's playlist
    const navigate = useNavigate();
    const [newPreference, setNewPreference] = useState({
        favorite_genre: '',
        favorite_artist: '',
        favorite_song: ''
    });

    const handleSignOut = () => {
        // Access the logout function from useAuth hook
        logout();
        navigate('/', { replace: true });
    };

    // Function to fetch preferences
    const fetchPreferences = async () => {
        try {
            const response = await axios.get(apiUrl, {
                headers: {
                    Authorization: `Bearer ${authToken}`,
                },
            });
            setPreferences(response.data);
            setLoading(false);
        } catch (error) {
            setError(error.response.data);
            setLoading(false);
        }
    };

     // Function to fetch user's playlist
    const fetchUserPlaylist = async () => {
        try {
            const response = await axios.get(playlistUrl, {
                headers: {
                    Authorization: `Bearer ${authToken}`,
                },
            });
            setUserPlaylist(response.data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching user playlist:', error);
            setLoading(false);
        }
    };

    useEffect(() => {
        if (authToken) {
            fetchPreferences();
            fetchUserPlaylist(); // Fetch user's playlist when component mounts
        }
    }, [authToken]);

 const handleSubmit = async (event) => {
    event.preventDefault();
    try {
        // Create or update the music preference
        await axios.post(apiUrl, newPreference, {
            headers: {
                Authorization: `Bearer ${authToken}`,
                'Content-Type': 'application/json',
            },
        });

        // Generate playlist
        await axios.post('http://127.0.0.1:8000/generate_playlist/', newPreference, {  // Send null instead of newPreference
            headers: {
                Authorization: `Bearer ${authToken}`,
                'Content-Type': 'application/json',
            },
        });

        // Fetch recommended songs
        const response = await axios.get(playlistUrl, {
            headers: {
                Authorization: `Bearer ${authToken}`,
            },
        });
        console.log('Recommended Songs Response:', response.data); // Debugging log
        setRecommendedSongs(response.data);

        // Refresh preferences after creating a new one
        fetchPreferences();
        setNewPreference({
            favorite_genre: '',
            favorite_artist: '',
            favorite_song: ''
        });
    } catch (error) {
        setError(error.response.data);
    }
};



    const handleDeletePreference = async () => {
        try {
            await axios.delete(apiUrl, {
                headers: {
                    Authorization: `Bearer ${authToken}`,
                },
            });
            // Refresh preferences after deleting
            fetchPreferences();
        } catch (error) {
            setError(error.response.data);
        }
    };

     const handleDeletePlaylist = async (playlistName) => {
        try {
            await axios.delete(playlistUrl, {
                headers: {
                    Authorization: `Bearer ${authToken}`,
                },
                // data: { name: playlistName } // Send the playlist name to be deleted
            });
            // Refresh user's playlist after deleting
            fetchUserPlaylist();
        } catch (error) {
            setError(error.response.data);
        }
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setNewPreference({
            ...newPreference,
            [name]: value
        });
    };

    return (
        <div>
            {loading && <p>Loading...</p>}
            {error && <p>Error: {error}</p>}
            {preferences && (
                <div>
                    <h2>Your Music Preferences</h2>
                    <ul>
                        <li>Favorite Genre: {preferences.favorite_genre}</li>
                        <li>Favorite Artist: {preferences.favorite_artist}</li>
                        <li>Favorite Song: {preferences.favorite_song}</li>
                    </ul>
                    <button onClick={handleDeletePreference}>Delete Preferences</button>
                </div>
            )}

             {/* Display user's playlist */}
            {userPlaylist && userPlaylist.length > 0 && (
            <div>
                <h2>Your Playlist</h2>
                <ul>
                    {userPlaylist.map((playlist, index) => (
                        <div key={index}>
                            <h3>{playlist.name}</h3>
                            <ul>
                                {playlist.tracks.map((track, trackIndex) => (
                                    <li key={trackIndex}>{track.name} - {track.artist}</li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </ul>
                {/* Optionally, you can add a button to delete the playlist */}
                 <button onClick={handleDeletePlaylist}>Delete Playlist</button>
            </div>
        )}

        {/*    {recommendedSongs.length > 0 && (*/}
        {/*    <div>*/}
        {/*        <h2>Recommended Songs</h2>*/}
        {/*        {recommendedSongs.map((playlist, index) => (*/}
        {/*            <div key={index}>*/}
        {/*                <h3>{playlist.name}</h3>*/}
        {/*                <ul>*/}
        {/*                    {playlist.tracks.map((track, trackIndex) => (*/}
        {/*                        <li key={trackIndex}>{track.name} - {track.artist}</li>*/}
        {/*                    ))}*/}
        {/*                </ul>*/}
        {/*            </div>*/}
        {/*        ))}*/}
        {/*    </div>*/}
        {/*)}*/}

            <h2>Create New Preferences</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="Favorite Genre" name="favorite_genre" value={newPreference.favorite_genre} onChange={handleChange} />
                <input type="text" placeholder="Favorite Artist" name="favorite_artist" value={newPreference.favorite_artist} onChange={handleChange} />
                <input type="text" placeholder="Favorite Song" name="favorite_song" value={newPreference.favorite_song} onChange={handleChange} />
                <button type="submit">Save Preferences and Generate Playlist</button>
            </form>

            <button onClick={handleSignOut}>Sign Out</button>
        </div>
    );
};

export default MusicPreferences;
