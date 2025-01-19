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

@app.get("/graphchart")
async def graph_chart():
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    values = [10, 14, 13, 25, 66, 29, 41, 52, 69, 60, 77, 88]
    
    # Цветовая палитра
    colors = ["#6c757d", "#6daedb", "#98d5ca", "#b8f5e0", "#005557"]

    # Создание диаграммы
    fig = go.Figure(data=[go.Line(x=labels, y=values)])

    # Настройка диаграммы
    fig.update_layout(
        title="Круговая диаграмма",
        template="plotly_dark"
    )

    # Сохранение диаграммы в HTML
    chart_path = os.path.join(os.getcwd(), "src/frontend/graph_chart.html")
    fig.write_html(chart_path)
    
    return FileResponse(chart_path)

@app.get("/{_filename}")
async def getfile(_filename: str):
    if _filename not in ["index.html", "styles.css", "pie_data", "graph_data", "favicon.ico"]:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    file = os.path.join(os.getcwd(), "src/frontend", _filename)
    return FileResponse(file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
