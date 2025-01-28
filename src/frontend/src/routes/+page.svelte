<script lang="ts">
    import { onMount } from "svelte";
    import { Chart } from "chart.js/auto";
    import { goto } from "$app/navigation";

    const email = "example@example.com";
    const phoneNumber = "+1234567890";

    type Strategies = {
        name: string,
        rating: number,
        cost: string,
        color: string
    };

    type Metrics = {
        pnl: number;
        sharp: number;
        profit_margin: number;
        max_drawdown: number;
        turnover: number;
    }

    let strategies: Strategies[];
    let metrics: Metrics | null = null;

    let incomeChartCanvas: HTMLCanvasElement | null = null;
    let allocationChartCanvas: HTMLCanvasElement | null = null;
    let incomeChart;
    let allocationChart;

    function navigateToLK() {
        goto('/lk'); // Перенаправление на страницу lk.svelte
    }

    onMount(async () => {
        let incomeChartLabels;
        let incomeChartValues;
        let allocationChartLabels;
        let allocationChartValues;

        const strategiesResponse = await fetch('/strategies');
        const strategiesData = await strategiesResponse.json();
        
        const incomeResponse = await fetch('/income');
        const incomeData = await incomeResponse.json();

        const allocationResponse = await fetch('/allocation');
        const allocationData = await allocationResponse.json();

        const metricsResponse = await fetch('/metrics');
        const metricsData = await metricsResponse.json();

        strategies = strategiesData.data;
        metrics = metricsData.data;

        incomeChartLabels = incomeData["labels"];
        incomeChartValues = incomeData["values"];

        allocationChartLabels = allocationData["labels"];
        allocationChartValues = allocationData["values"];

        if (incomeChartCanvas) {
            const incomeContext = incomeChartCanvas.getContext('2d');
            if (!incomeContext) return;

            incomeChart = new Chart(incomeContext, {
                type: 'line',
                data: {
                    labels: incomeChartLabels,
                    datasets: [{
                        label: 'Доходность',
                        data: incomeChartValues
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgb(38 38 38)'
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgb(38 38 38)'
                            }
                        }
                    }
                }
            })
        }

        if (allocationChartCanvas) {
            const allocationContext = allocationChartCanvas.getContext('2d');
            if (!allocationContext) return;

            allocationChart = new Chart(allocationContext, {
                type: 'pie',
                data: {
                    labels: allocationChartLabels,
                    datasets: [{
                        data: allocationChartValues
                    }]
                },
                options: {
                    responsive: true,
                    aspectRatio: 2,
                    plugins: {
                        legend: {
                            /*position: 'right',
                            labels: {
                                color: 'rgb(255, 255, 255)',
                                boxHeight: 15,
                                padding: 15
                            }*/
                            display: false
                        }
                    },
                    layout: {
                        padding: 10
                    }
                }
            })
        }
    });
</script>


<main class="bg-neutral-800 min-h-screen text-white">
    <div class="mx-auto max-w-6xl py-6">
        <!-- Добавленная кнопка -->
        <div class="flex justify-end mb-4">
            <button
                on:click={navigateToLK}
                class="bg-teal-500 hover:bg-teal-400 text-neutral-900 font-semibold px-6 py-2 rounded-lg border border-teal-700 shadow-lg transition-all"
            >
                Подключиться
            </button>
        </div>

        <section class="py-12">
            <div class="grid grid-cols-2 gap-4">
                <div class="flex p-6 bg-neutral-900 rounded-lg flex-col gap-2">
                    <h1 class="text-xl">Выбранная стратегия</h1>
                    <div>
                        <table class="min-w-full table-auto">
                            <thead>
                                <tr>
                                    <th class="px-2 py-2 text-left">#</th>
                                    <th class="px-2 py-2 text-left">Стратегия</th>
                                    <th class="px-2 py-2 text-left">Оценка пользователей</th>
                                    <th class="px-2 py-2 text-left">Емкость</th>
                                </tr>
                            </thead>
                            <tbody>
                                {#each strategies as { name, rating, cost, color }, index}
                                <tr>
                                    <td class="px-2 py-1">{index + 1}</td>
                                    <td class="px-2 py-1">{name}</td>
                                    <td class="px-2 py-1">
                                        <div class="w-full h-4 bg-neutral-800 rounded-full">
                                            <div style="width: { rating }%;" class="{ color } h-full rounded-full"></div>
                                        </div>
                                    </td>
                                    <td class="px-2 py-1">{cost}</td>
                                </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="flex p-4 bg-neutral-900 rounded-lg flex-col gap-2">
                    <h1 class="text-xl">Метрики</h1>
                    <div class="flex flex-col min-w-full gap-2">
                        <div class="flex flex-row justify-between">
                            <p>Доход: </p>
                            <div class="bg-teal-600 px-2 rounded-lg"><p>{ metrics?.pnl ?? '?' }</p></div>
                        </div>
                        <div class="flex flex-row justify-between">
                            <p>Стабильность:</p>
                            <div class="bg-teal-600 px-2 rounded-lg"><p>{ metrics?.sharp ?? '?' }</p></div>
                        </div>
                        <div class="flex flex-row justify-between">
                            <p>Эффективность использования капитала:</p>
                            <div class="bg-teal-600 px-2 rounded-lg"><p>{ metrics?.profit_margin ?? '?' }</p></div>
                        </div>
                        <div class="flex flex-row justify-between">
                            <p>Максимальная просадка:</p>
                            <div class="bg-teal-600 px-2 rounded-lg"><p>{ metrics?.max_drawdown ?? '?' }</p></div>
                        </div>
                        <div class="flex flex-row justify-between">
                            <p>Активность торговли:</p>
                            <div class="bg-teal-600 px-2 rounded-lg"><p>{ metrics?.turnover ?? '?' }</p></div>
                        </div>
                    </div>
                </div>
                <div class="flex p-6 bg-neutral-900 rounded-lg flex-col gap-2">
                    <h1 class="text-xl text-white">График доходности, %</h1>
                    <canvas bind:this={ incomeChartCanvas } id="incomeChart"></canvas>
                </div>
                <div class="flex p-6 bg-neutral-900 rounded-lg flex-col gap-2">

                    <h1 class="text-xl text-white">Распределение средств по активам</h1>
                    <canvas bind:this={ allocationChartCanvas } id="allocationChart"></canvas>
                </div>
            </div>
        </section>
        <footer class="flex bg-neutral-900 p-6 rounded-lg justify-between">
            <p>Контактная информация: <a href="mailto:{ email }" class="text-blue-300 hover:text-blue-400">{ email }</a> | { phoneNumber }</p>
            <p><a href="https://google.com" class="text-blue-300 hover:text-blue-400">Пользовательское соглашение</a></p>
        </footer>
    </div>
</main>