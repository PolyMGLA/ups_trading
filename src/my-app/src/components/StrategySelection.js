import React from 'react';
import './StrategySelection.css';

const StrategySelection = () => {
  return (
    <div className="strategy-selection">
      <h2>Выбор стратегии</h2>
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Стратегия</th>
            <th>Оценка пользователей</th>
            <th>Ёмкость</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>01</td>
            <td>Anti-mainstream 1</td>
            <td><div className="bar orange" /></td>
            <td>$46.000</td>
          </tr>
          <tr>
            <td>02</td>
            <td>Anti-mainstream 2</td>
            <td><div className="bar blue" /></td>
            <td>$17.000</td>
          </tr>
          <tr>
            <td>03</td>
            <td>Anti-mainstream 3</td>
            <td><div className="bar cyan" /></td>
            <td>$19.000</td>
          </tr>
          <tr>
            <td>04</td>
            <td>Anti-mainstream 4</td>
            <td><div className="bar pink" /></td>
            <td>$29.000</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default StrategySelection;