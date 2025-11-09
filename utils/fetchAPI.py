import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Szkoda gadać (funkcja do pobierania tokena w osobnym wątku bo requests jest blokujące)
async def fetchToken(password, username):
    loop = asyncio.get_event_loop()
    def req():
        return requests.post('https://kazachstan.servebeer.com/login', json={"username": username, "password": password})
    with ThreadPoolExecutor() as pool:
        response = await loop.run_in_executor(pool, req)
    return response

# Disappearing emoji meme (funkcja do pobierania odpowiedzi z API w osobnym wątku bo requests jest blokujące)
async def fetchAPI(prompt, token=None):
    loop = asyncio.get_event_loop()
    def req():
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": token
        }
        json = {
            "contents": [
                {"parts": [{"text": f"Odpowiadaj po Polsku: {prompt}"}]}
            ]
        }
        return requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            headers=headers,
            json=json
        )
    with ThreadPoolExecutor() as pool:
        response = await loop.run_in_executor(pool, req)
    return response
