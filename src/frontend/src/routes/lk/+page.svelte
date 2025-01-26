<script>
    import { onMount } from 'svelte';
  
    let username = "Иван Смирнов";
    let balance = 112000;
    let profit = 12000;
  
    const strategies = [
      { name: "Стратегия 1", result: 12, positive: true },
    ];
  
    function logout() {
      window.location.href = 'main';
    }
  </script>
  
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: #30313A;
      color: #30313A;
    }
  
    .account-page {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
      background-color: #30313A;
      color: white;
    }
  
    .account-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      color: white;
    }
  
    .user-info {
      display: flex;
      align-items: center;
    }
  
    .avatar {
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background-color: #70c1b3;
      margin-right: 10px;
    }
  
    .username {
      font-size: 18px;
      font-weight: bold;
      color: #f0f0f0;
      background-color: #30313A;
    }
  
    .logout-btn {
      background-color: #ff6b6b;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }
  
    .logout-btn:hover {
      background-color: #e05656;
    }
  
    .balance-section {
      text-align: left;
      margin-bottom: 40px;
    }
  
    .balance-text {
      font-size: 20px;
      font-weight: bold;
    }
  
    .green {
      color: #70c1b3;
    }
  
    .red {
      color: #ff6b6b;
    }
  
    .strategies-section {
      text-align: center;
    }
  
    .section-title {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 20px;
    }
  
    .strategies-list {
      list-style: none;
      padding: 0;
    }
  
    .strategy-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background-color: #21222D;
      border: 1px solid #40424e;
      border-radius: 8px;
      padding: 10px 20px;
      margin: 10px 0;
      font-size: 18px;
    }
  
    .strategy-name {
      font-weight: bold;
      color: #f0f0f0;
      background-color: #30313A;
    }
  
    .strategy-result {
      font-weight: bold;
    }
  
    footer {
      background-color: #21222D;
      color: white;
      padding: 10px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #30313A;
      font-size: 14px;
    }
  
    footer .agreement-link a {
      color: #a9dfd8;
      text-decoration: none;
      padding: 4px 8px;
      border-radius: 4px;
    }
  
    footer .agreement-link a:hover {
      background-color: rgba(169, 223, 216, 0.2);
    }
  </style>
  
  <div class="account-page">
    <header class="account-header">
      <div class="user-info">
        <div class="avatar"></div>
        <span class="username">{username}</span>
      </div>
      <button class="logout-btn" on:click={logout}>Выйти из аккаунта</button>
    </header>
  
    <div class="balance-section">
      <p class="balance-text">
        Ваш баланс: $ {balance.toLocaleString()} <span class="profit {profit > 0 ? 'green' : 'red'}">({profit > 0 ? '+' : ''}$ {profit.toLocaleString()})</span>
      </p>
    </div>
  
    <div class="strategies-section">
      <h2 class="section-title">Мои стратегии</h2>
      <ul class="strategies-list">
        {#each strategies as strategy}
          <li class="strategy-item">
            <span class="strategy-name">{strategy.name}</span>
            <span class="strategy-result {strategy.positive ? 'green' : 'red'}">
              {strategy.positive ? '+' : ''}{strategy.result}%
            </span>
          </li>
        {/each}
      </ul>
    </div>
  </div>
  
  <footer>
    <div class="contact-info">
      <p>Контактная информация: example@example.com | +123 456 7890</p>
    </div>
    <div class="agreement-link">
      <a href="https://www.youtube.com" target="_blank">Пользовательское соглашение</a>
    </div>
  </footer>
  