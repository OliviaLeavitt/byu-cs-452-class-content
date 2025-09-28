import argparse
from db import create_connection, query_sql

def query_sql(connection, sql, params=()):
    cur = connection.cursor()
    cur.execute(sql, params)
    return cur.fetchall()

def print_rows(rows):
    if not rows:
        print("No rows found.")
        return
    for row in rows:
        print(row)

def select_from_table(conn, query):
    rows = query_sql(conn, query)
    print_rows(rows)

def all_recipes(conn):
    sql = "SELECT recipe_id, name, difficulty FROM Recipe"
    print("All Recipes:")
    select_from_table(conn, sql)

def recipes_by_baker(conn, baker_name):
    sql = f"""
        SELECT Recipe.recipe_id, Recipe.name, Recipe.difficulty 
        FROM Recipe
        JOIN Baker ON Recipe.baker_id = Baker.baker_id
        WHERE Baker.name = '{baker_name}'
    """
    print(f"Recipes by {baker_name}:")
    select_from_table(conn, sql)

def ingredients_for_recipe(conn, recipe_name):
    sql = f"""
        SELECT Ingredient.name, RecipeIngredient.amount 
        FROM Ingredient
        JOIN RecipeIngredient ON Ingredient.ingredient_id = RecipeIngredient.ingredient_id
        JOIN Recipe ON Recipe.recipe_id = RecipeIngredient.recipe_id
        WHERE Recipe.name = '{recipe_name}'
    """
    print(f"Ingredients for {recipe_name}:")
    select_from_table(conn, sql)

def reviews_for_recipe(conn, recipe_name):
    sql = f"""
        SELECT reviewer_name, rating, comment
        FROM Review rev
        JOIN Recipe ON rev.recipe_id = Recipe.recipe_id
        WHERE Recipe.name = '{recipe_name}'
    """
    print(f"Reviews for {recipe_name}:")
    select_from_table(conn, sql)

if __name__ == "__main__":
    database = "./baking.sqlite"
    conn = create_connection(database)

    parser = argparse.ArgumentParser()
    parser.add_argument("--query_type", type=str, required=True, help="Type of query: all, baker, ingredients, reviews")
    parser.add_argument("--name", type=str, help="Name for baker or recipe")
    args = parser.parse_args()

    if args.query_type == "all":
        all_recipes(conn)
    elif args.query_type == "baker" and args.name:
        recipes_by_baker(conn, args.name)
    elif args.query_type == "ingredients" and args.name:
        ingredients_for_recipe(conn, args.name)
    elif args.query_type == "reviews" and args.name:
        reviews_for_recipe(conn, args.name)
    else:
        print("Invalid query_type or missing name argument.")

    if conn:
        conn.close()
