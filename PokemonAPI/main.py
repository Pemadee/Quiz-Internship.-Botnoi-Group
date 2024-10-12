from fastapi import FastAPI
# from pydantic import BaseModel
import httpx

app = FastAPI()


@app.post("/get-pokemon/")
async def get_pokemon():
    async with httpx.AsyncClient() as client:
      
        pokemon_response = await client.get(f"https://pokeapi.co/api/v2/pokemon/1/")
        pokemon_data = pokemon_response.json()

        required_urls = ["https://pokeapi.co/api/v2/stat/1/", "https://pokeapi.co/api/v2/stat/2/"]
        filtered_stats = []
        for stat in pokemon_data.get("stats", []):
            if stat["stat"]["url"] in required_urls:
                filtered_stats.append(stat)
      
        pokemon_form_response = await client.get(f"https://pokeapi.co/api/v2/pokemon-form/1/")
        pokemon_form_data = pokemon_form_response.json()

        name = pokemon_form_data.get("name", "")
        sprites = pokemon_form_data.get("sprites", {})

        combined_data = {
            "stats": filtered_stats,
            "name": name,
            "sprites": sprites
        }
        return combined_data
        

# Command: uvicorn main:app --reload
