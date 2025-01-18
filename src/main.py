from fastapi import FastAPI
from starlette.responses import Response, FileResponse, HTMLResponse
from starlette import status
import plotly.graph_objects as go
import os

app = FastAPI()

@app.get("/")
async def index():
    file = os.path.join(os.getcwd(), "src/frontend/index.html")
    return FileResponse(file)

@app.get("/ping")
async def ping():
    return Response(status_code=status.HTTP_200_OK)

@app.get("/{_filename}")
async def getfile(_filename: str):
    file = os.path.join(os.getcwd(), "src/frontend", _filename)
    return FileResponse(file)

@app.get("/piechart")
async def pie_chart():
    # Данные для круговой диаграммы
    labels = ["Категория A", "Категория B", "Категория C", "Категория D"]
    values = [40, 30, 20, 10]
    
    # Цветовая палитра
    colors = ["#6c757d", "#6daedb", "#98d5ca", "#b8f5e0", "#005557"]

    # Создание диаграммы
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])

    # Настройка диаграммы
    fig.update_layout(
        title="Круговая диаграмма",
        template="plotly_dark"
    )

    # Сохранение диаграммы в HTML
    chart_path = os.path.join(os.getcwd(), "src/frontend/pie_chart.html")
    fig.write_html(chart_path)

    return FileResponse(chart_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
