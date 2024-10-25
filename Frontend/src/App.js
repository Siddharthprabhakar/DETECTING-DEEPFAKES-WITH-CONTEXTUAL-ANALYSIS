import React, { Component } from 'react';
import './App.css';
import 'aos/dist/aos.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './Pages/index';

class App extends Component {
  render() {
    return (
      <Router>
        <Routes>
          <Route path='/' element={<Home />} exact />
        </Routes>
      </Router>
    );
  }
}

export default App;
