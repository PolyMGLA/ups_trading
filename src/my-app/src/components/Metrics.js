import React from 'react';
import './Metrics.css';

const Metrics = () => {
  return (
    <div className="metrics">
      <h2>Метрики</h2>
      <ul>
        <li>
          PnL: <span className="metric-box">46%</span>
        </li>
        <li>
          Sharp: <span className="metric-box">46%</span>
        </li>
        <li>
          Profit margin: <span className="metric-box">46%</span>
        </li>
        <li>
          Max Drawdown: <span className="metric-box">46%</span>
        </li>
        <li>
          Turnover: <span className="metric-box">46%</span>
        </li>
      </ul>
    </div>
  );
};

export default Metrics;
