from typing import Optional
from pydantic import BaseModel, HttpUrl
from fastapi import FastAPI, APIRouter, Query


app = FastAPI(
    title='Recipe API',
    description='Recipe API',
    version='1.0.0',
)

api_router = APIRouter()


class Recipe(BaseModel):
    id: int
    label: str
    source: str
    url: HttpUrl


RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]


@api_router.get('/', status_code=200)
def root() -> dict:
    return {'msg': 'hello world'}


@api_router.get('/recipe/{recipe_id}', status_code=200)
def fetch_recipe(recipe_id):
    result = [recipe for recipe in RECIPES if recipe['id']==recipe_id]
    return result[0]


@api_router.get('/search/', status_code=200, summary='测试')
def search_recipe(
    keywords: Optional[str] = Query(None, min_length=3, example='chicken'),
    max_result: Optional[int]=10
):
    if not keywords:
        return {'results': RECIPES[:max_result]}
    results = filter(lambda recipe: keywords.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_result]}


app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, workers=1)