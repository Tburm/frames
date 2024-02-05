import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.images import resize_png
from src.data import get_volume, get_oi
from src.charts import chart_bars, chart_lines
from src.cache import Cache

# initialize the cache
cache = Cache()

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get('/moonbird', response_class=HTMLResponse)
async def moonbird():
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
async def volume():
    chart_name = "volume"
    
    if cache.needs_update(chart_name):
        # regenerate chart
        df = get_volume()
        chart = chart_bars(df, "ts", "volume", "SNX V3 Perps - Daily Volume", color="market_symbol",)
        chart.write_image("images/volume.png")
        cache.update_chart_time(chart_name)

    # serve the content
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta property="og:title" content="Frame" />
            <meta property="fc:frame" content="vNext" />
            <meta property="fc:frame:image" content="https://data.gbv.dev/frame/images/volume.png" />
            <meta property="og:image" content="https://data.gbv.dev/frame/images/volume.png" />
            <meta property="fc:frame:post_url" content="https://data.gbv.dev/frame/" />
            <meta property="fc:frame:button:1" content="Volume" />
            <meta property="fc:frame:button:2" content="Open Interest" />
            <meta property="fc:frame:button:3" content="More Data" />
            <meta property="fc:frame:button:3:action" content="post_redirect" />
        </head>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get('/oi', response_class=HTMLResponse)
async def oi():
    chart_name = "oi"
    
    if cache.needs_update(chart_name):
        # regenerate chart
        df = get_oi()
        chart = chart_lines(df, "ts", "size_usd", "SNX V3 Perps - Open Interest", color="market_symbol",)
        chart.write_image("images/oi.png")
        cache.update_chart_time(chart_name)

    # serve the content
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta property="og:title" content="Frame" />
            <meta property="fc:frame" content="vNext" />
            <meta property="fc:frame:image" content="https://data.gbv.dev/frame/images/oi.png" />
            <meta property="og:image" content="https://data.gbv.dev/frame/images/oi.png" />
            <meta property="fc:frame:post_url" content="https://data.gbv.dev/frame/" />
            <meta property="fc:frame:button:1" content="Volume" />
            <meta property="fc:frame:button:2" content="Open Interest" />
            <meta property="fc:frame:button:3" content="More Data" />
            <meta property="fc:frame:button:3:action" content="post_redirect" />
        </head>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post('/', response_class=HTMLResponse)
async def redirect(request: Request):
    request_json = await request.json()
    
    if not 'untrustedData' in request_json:
        raise HTTPException(status_code=400, detail="Missing untrustedData")
    
    data = request_json['untrustedData']
    button_index = data.get('buttonIndex')
    
    # Internal dispatch based on button_index
    if button_index == 1:
        return await volume()
    elif button_index == 2:
        return await oi()
    elif button_index == 3:
        return RedirectResponse(url="https://synthetix.streamlit.app/Base%20Mainnet", status_code=302)
    else:
        raise HTTPException(status_code=400, detail="Invalid buttonIndex")
