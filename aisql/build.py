import os
from db import create_table, create_connection
from schema import *

def insert_bakers(connection):
    sql = """
    INSERT INTO Baker (baker_id, name, experience_level) VALUES
    (1, 'Olivia Leavitt', 'Intermediate'),
    (2, 'Paul Hollywood', 'Expert'),
    (3, 'Gordon Ramsey', 'Expert'),
    (4, 'Mary Berry', 'Expert');
    """
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def insert_recipes(connection):
    sql = """
    INSERT INTO Recipe (recipe_id, name, description, baking_time_minutes, difficulty, baker_id) VALUES
    (1, 'Chocolate Cake', 'Rich and moist', 60, 'Medium', 1),
    (2, 'Sourdough Bread', 'A yummy loaf', 180, 'Hard', 2),
    (3, 'Banana Muffins', 'Soft and fluffy', 30, 'Easy', 4);
    """
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def insert_ingredients(connection):
    sql = """
    INSERT INTO Ingredient (ingredient_id, name, category) VALUES
    (1, 'Flour', 'Dry'),
    (2, 'Sugar', 'Dry'),
    (3, 'Eggs', 'Wet'),
    (4, 'Butter', 'Wet'),
    (5, 'Chocolate', 'Flavoring'),
    (6, 'Banana', 'Fruit');
    """
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def insert_recipeIngredients(connection):
    sql = """
    INSERT INTO RecipeIngredient (recipe_id, ingredient_id, amount) VALUES
    (1, 1, '200g'),
    (1, 2, '150g'),
    (1, 3, '3 units'),
    (1, 4, '100g'),
    (1, 5, '50g'),
    (3, 1, '150g'),
    (3, 2, '80g'),
    (3, 3, '2 units'),
    (3, 6, '2 units');
    """
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def insert_categories(connection):
    sql = """
    INSERT INTO Category (category_id, name) VALUES
    (1, 'Dessert'),
    (2, 'Bread'),
    (3, 'Breakfast');
    """
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def insert_recipeCategories(connection):
    sql = """
    INSERT INTO RecipeCategory (recipe_id, category_id) VALUES
    (1, 1),
    (2, 2),
    (3, 3);
    """
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def insert_reviews(connection):
    sql = """
    INSERT INTO Review (review_id, recipe_id, reviewer_name, rating, comment) VALUES
    (1, 1, 'Amy', 5, 'Delicious!'),
    (2, 2, 'Tanner', 4, 'Great crust, a bit wet'),
    (3, 3, 'Charlie', 5, 'I love muffins');
    """
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def insert_bakeEvents(connection):
    sql = """
    INSERT INTO BakeEvent (event_id, baker_id, recipe_id, bake_date) VALUES
    (1, 1, 1, '2025-09-27'),
    (2, 2, 2, '2025-09-28'),
    (3, 4, 3, '2025-09-29');
    """
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def main():
    connection = create_connection("baking.sqlite")

    create_table(connection, sql_create_baker_table)
    create_table(connection, sql_create_recipe_table)
    create_table(connection, sql_create_ingredient_table)
    create_table(connection, sql_create_recipeIngredient_table)
    create_table(connection, sql_create_category_table)
    create_table(connection, sql_create_recipeCategory_table)
    create_table(connection, sql_create_review_table)
    create_table(connection, sql_create_bakeEvent_table)

    insert_bakers(connection)
    insert_recipes(connection)
    insert_ingredients(connection)
    insert_recipeIngredients(connection)
    insert_categories(connection)
    insert_recipeCategories(connection)
    insert_reviews(connection)
    insert_bakeEvents(connection)

    print("Database created.")

if __name__ == "__main__":
    main()
