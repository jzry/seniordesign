import axios from 'axios'
import logo from './logo.svg';
import './App.css';

const getData = () => {
  axios.get('http://localhost:8080')
    .then((data) => {
      console.log(data)
    })
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <button onClick={getData}>Get Data</button>
      </header>
    </div>
  );
}

export default App;
