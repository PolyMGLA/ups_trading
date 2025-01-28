<script>
  function goBack() {
    window.location.href = '/';
  }
</script>

<style>
  body {
    font-family: Arial, sans-serif;
    background-color: #121212;
    color: #FFFFFF;
    margin: 0;
    padding: 0;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: #1F1F1F;
  }

  .back-button {
    padding: 10px 20px;
    border: none;
    background-color: #b1f5ec;
    color: #121212;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    border: 2px solid #7daea7e0;
  }

  .strategy-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px;
  }

  .strategy-card {
    background-color: #1F1F1F;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    border: 1px solid #b1f5ec;
  }

  .strategy-card h3 {
    color: #b1f5ec;
    margin-bottom: 10px;
  }

  .footer {
    text-align: center;
    padding: 20px;
    background-color: #1F1F1F;
    border-top: 1px solid #b1f5ec;
  }
</style>

<header class="header">
  <button class="back-button" on:click={goBack}>⬅ Назад</button>
  <h2>Подобранные стратегии</h2>
</header>

<main>
  <section class="strategy-cards">
    <div class="strategy-card">
      <h3>RostOK</h3>
      <p>Подписчики: 50</p>
      <p>Минимальная сумма: $300</p>
      <p>Среднегодовая доходность: 25.8%</p>
      <p>Прогнозируемая просадка: -12%</p>
    </div>
    <div class="strategy-card">
      <h3>x2</h3>
      <p>Подписчики: 30</p>
      <p>Минимальная сумма: $200</p>
      <p>Среднегодовая доходность: 30.5%</p>
      <p>Прогнозируемая просадка: -18%</p>
    </div>
  </section>
</main>

<footer class="footer">
  <p>© 2025 MoneyButtonAI</p>
</footer>
