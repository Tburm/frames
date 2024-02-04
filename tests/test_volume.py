import requests

def test_volume(logger):
    url = 'http://localhost:8000/volume'
    
    response = requests.get(url)
    logger.info(response.text)
    assert response.status_code == 200
    assert 'volume' in response.text
    assert 'og:image' in response.text
    assert 'fc:frame' in response.text
    assert 'fc:frame:image' in response.text
    