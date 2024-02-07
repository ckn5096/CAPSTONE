import logo from './logo.svg';
import './App.css';
import React from 'react';
import { Link } from 'react-router-dom';


function App() {
  /*
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );

   */

  return (
    <div>
      <h1>Welcome to Music Match</h1>
        {/* Signup button */}
      < Link to = "/Registration" >
          <button> SignUp </button>
          </Link>
        < Link to = "/Login" >
          <button> Login </button>
          </Link>
    </div>
  );
}

export default App;
