import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.images import resize_png
from src.data import get_volume
from src.charts import chart_bars

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get('/moonbird', response_class=HTMLResponse)
def moonbird():
    # check if file exists
    if not os.path.exists('./images/moonbird.png'):
        resize_png('./images/raw/moonbird.png', './images/moonbird.png')

    # serve the content
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta property="og:title" content="Frame" />
            <meta property="fc:frame" content="vNext" />
            <meta property="fc:frame:image" content="https://data.gbv.dev/frame/images/moonbird.png" />
            <meta property="og:image" content="https://data.gbv.dev/frame/images/moonbird.png" />
        </head>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get('/volume', response_class=HTMLResponse)
def volume():
    # static values
    content = "SNX V3 Base"
    
    # get the content
    df = get_volume()
    chart = chart_bars(df, "ts", "volume", "SNX Perps: Daily Volume")
    
    # write it
    chart.write_image("images/volume.png")

    # serve the content
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta property="og:title" content="Frame" />
            <meta property="fc:frame" content="vNext" />
            <meta property="fc:frame:image" content="https://data.gbv.dev/frame/images/volume.png" />
            <meta property="og:image" content="https://data.gbv.dev/frame/images/volume.png" />
            <meta property="fc:frame:input:text" content="{content}" />
        </head>
    </html>
    """
    return HTMLResponse(content=html_content)

