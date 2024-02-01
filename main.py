from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def frame():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta property="fc:frame" content="vNext" />
            <meta property="fc:frame:image" content="https://proof-nft-image.imgix.net/0x23581767a106ae21c074b2276D25e5C3e136a68b/5833?auto=format&ixlib=react-9.5.1-beta.1&w=1440" />
        </head>
    </html>
    """
    return HTMLResponse(content=html_content)
