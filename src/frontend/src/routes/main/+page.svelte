<script>
    // Логика обработки (в данном случае, переход по ссылке можно оставить без изменений)
    function redirectToPage() {
      window.location.href = '/';
    }
  </script>
  
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: #30313A;
      color: #30313A;
    }
  
    .welcome-page {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 85vh;
      text-align: center;
      background-color: #30313A;
    }
  
    .welcome-content {
      max-width: 800px;
    }
  
    .main-title {
      font-size: 52px;
      font-weight: bold;
      color: #70c1b3;
      margin-bottom: 10px;
    }
  
    .tagline {
      font-size: 20px;
      color: #b1f5ec;
      margin-bottom: 20px;
    }
  
    .description {
      font-size: 22px;
      color: #f0f0f0;
      line-height: 1.6;
      margin-bottom: 30px;
    }
  
    .screening-intro {
      font-size: 18px;
      color: #a9dfd8;
      margin-bottom: 20px;
    }
  
    .btn-select-strategy {
      background-color: #70c1b3;
      color: #fff;
      border: none;
      padding: 12px 24px;
      font-size: 18px;
      font-weight: bold;
      border-radius: 8px;
      cursor: pointer;
      transition: background-color 0.3s ease, transform 0.2s ease;
    }
  
    .btn-select-strategy:hover {
      background-color: #4f8aa6;
      transform: scale(1.05);
    }
  
    footer {
      background-color: #21222d;
      color: white;
      padding: 10px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #30313a;
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

    .main {
        background-color: #30313A;
    }
    p {
        font-size: 25px;
    }
  </style>
<main class="main">
  <div class="welcome-page" style="background-color: #30313A">
    <div class="welcome-content">
      <h2 class="main-title">Алгоритмическая торговля портфелем криптовалют на основе ML и NLP</h2>
      <p class="tagline">Комплекс ПО, позволяющий эффективно вложить средства</p>
      <p class="description">
        Платформа для инвесторов, предполагающая выбор стратегии по параметрам риска и доходности и непосредственно реализующая торговлю деньгами инвесторов при помощи алгоритмов, реализованных в рамках смены.
      </p>
      <p class="screening-intro">Подберите стратегию по своим запросам с помощью скринера</p>
      <button class="btn-select-strategy" on:click={redirectToPage}>Подобрать</button>
    </div>
  </div>
  
  <footer class="footer">
    <div class="contact-info">
      <p>Контактная информация: example@example.com | +123 456 7890</p>
    </div>
    <div class="agreement-link">
      <a href="https://www.youtube.com" target="_blank">Пользовательское соглашение</a>
    </div>
  </footer>
</main>