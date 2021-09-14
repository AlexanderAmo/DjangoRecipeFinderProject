from py_edamam import Edamam
from recipes.models import Recipe
# https://github.com/JarbasAl/py_edamam old version

APP_ID = '5c34d9a2'
APP_KEY = 'cfc8298a0c6fbe12210d054cc0d3ebc0'


def get_recipe(query):
  Edo_object = findRecipe(recipes_appid=APP_ID,recipes_appkey=APP_KEY,)
  Recipe_URLS = []
  recipeIngr = ''

  for recipe in Edo_object.search_recipe(query):

    for ingr in recipe.ingredient_names:
      recipeIngr += ingr

    Recipe_URLS.append(recipe.url)

    recipe_data = Recipe(
      recipeLabel = recipe.label,
      recipeLink = recipe.url,
      recipeIngredients = recipeIngr,
      recipeImageLink = recipe.image
    )
    if(recipe_data.isUnique()):
      recipe_data.save()
    else:
      pass
  

# copied from https://github.com/JarbasAl/py_edamam
class findRecipe(Edamam):

  def search_recipe(self, query):
    data = super().search_recipe(query)
    hits = data["hits"]
    for hit in hits:
      data = hit["recipe"]
      data["yields"] = data["yield"]
      data.pop("yield")
      data["ingredient_names"] = data["ingredientLines"]
      data.pop("ingredientLines")
      data["share_url"] = data["shareAs"]
      data.pop("shareAs")
      yield aRecipe(edamam=self, **data)

# copied from https://github.com/JarbasAl/py_edamam
# added cuisineType, mealType, and dishType because This library for the API was 
# created 2 years ago and I guess they updated the API, but the library creator
# never updated the library.
class aRecipe:
    def __init__(self,
                 label,
                 cuisineType = "",
                 mealType = "",
                 dishType="",
                 uri="",
                 url="",
                 share_url="",
                 image=None,
                 dietLabels=None,
                 healthLabels=None,
                 yields=1.0,
                 cautions=None,
                 totalDaily=None,
                 totalWeight=0,
                 calories=0,
                 totalTime=0,
                 totalNutrients=None,
                 digest=None,
                 ingredients=None,
                 source="edamam",
                 ingredient_names=None,
                 edamam=None):
        self.cuisineType = cuisineType or []
        self.mealType = mealType or []
        self.dishType = dishType or []
        self.ingredient_names = ingredient_names or []
        self.ingredient_quantities = ingredients or []
        self.label = label
        self.dietLabels = dietLabels or []
        self.healthLabels = healthLabels or []
        self.uri = uri
        self.url = url or self.uri
        self.share_url = share_url or self.url
        self.yields = yields
        self.cautions = cautions
        self.totalDaily = totalDaily or []

        self.totalWeight = totalWeight
        self.calories = calories
        self.totalTime = totalTime
        self.totalNutrients = totalNutrients or []

        self.image = image
        if isinstance(digest, list):
            self.digest = {}
            for content in digest:
                self.digest[content["label"]] = content
        else:
            self.digest = digest or {}
        self.__edamam = edamam or Edamam()

    def get_ingredients_data(self):
        for ing in self.__edamam.search_nutrient(self.ingredient_names):
            yield ing

    def __str__(self):
        return self.label












