from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageOps

def resize_and_crop_image(input_path, output_path, aspect_ratio=1.91):
    # Open the input image
    with Image.open(input_path) as image:
        original_width, original_height = image.size
        target_width = original_width
        target_height = int(target_width / aspect_ratio)

        # Calculate padding needed to achieve aspect ratio
        if original_height < target_height:
            # Case: Image is too wide
            padding_top = (target_height - original_height) // 2
            padding_bottom = target_height - original_height - padding_top
            padding_left = 0
            padding_right = 0
        else:
            # Case: Image is too tall or has the correct height
            target_height = original_height
            target_width = int(target_height * aspect_ratio)
            padding_left = (target_width - original_width) // 2
            padding_right = target_width - original_width - padding_left
            padding_top = 0
            padding_bottom = 0

        # Apply padding
        image = ImageOps.expand(image, (padding_left, padding_top, padding_right, padding_bottom), fill='black')
        
        # Optionally, if you want to ensure the image is exactly the target size, you can then crop it:
        # This is typically not needed if the calculations above are correct
        # image = image.crop((0, 0, target_width, target_height))

        # Save the output image
        image.save(output_path, 'PNG')

app = FastAPI()

app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get('/moonbird', response_class=HTMLResponse)
def frame():
    resize_and_crop_image('./images/raw/moonbird.png', './images/moonbird.png')

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
