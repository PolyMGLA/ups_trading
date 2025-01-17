import React from 'react';
import StrategySelection from './components/StrategySelection';
import Metrics from './components/Metrics';
import PerformanceChart from './components/PerformanceChart';
import SectorsChart from './components/SectorsChart';
import Footer from './components/Footer';
import './App.css';

const App = () => {
  return (
    <div className="dashboard">
      <div className="row">
        <StrategySelection />
        <Metrics />
      </div>
      <div className="row">
        <PerformanceChart />
        <SectorsChart />
      </div>
      <Footer />
    </div>
  );
};

export default App;