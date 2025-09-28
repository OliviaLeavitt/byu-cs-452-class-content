sql_create_baker_table = """ 
CREATE TABLE Baker (
  baker_id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  experience_level TEXT CHECK (experience_level IN ('Beginner', 'Intermediate', 'Expert'))
);
"""

sql_create_recipe_table = """ 
CREATE TABLE Recipe (
  recipe_id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  baking_time_minutes INT,
  difficulty TEXT CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
  baker_id INT,
  FOREIGN KEY (baker_id) REFERENCES Baker(baker_id)
);
"""

sql_create_ingredient_table = """
CREATE TABLE Ingredient (
  ingredient_id INTEGER PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  category VARCHAR(50)
);
"""

sql_create_recipeIngredient_table = """
CREATE TABLE RecipeIngredient (
  recipe_id INT,
  ingredient_id INT,
  amount VARCHAR(50),
  PRIMARY KEY (recipe_id, ingredient_id),
  FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),
  FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id)
);
"""

sql_create_category_table = """
CREATE TABLE Category (
  category_id INTEGER PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);
"""

sql_create_recipeCategory_table = """
CREATE TABLE RecipeCategory (
  recipe_id INT,
  category_id INT,
  PRIMARY KEY (recipe_id, category_id),
  FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),
  FOREIGN KEY (category_id) REFERENCES Category(category_id)
);
"""

sql_create_review_table = """
CREATE TABLE Review (
  review_id INTEGER PRIMARY KEY,
  recipe_id INT,
  reviewer_name VARCHAR(100),
  rating INT CHECK (rating BETWEEN 1 AND 5),
  comment TEXT,
  FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id)
);
"""

sql_create_bakeEvent_table = """
CREATE TABLE BakeEvent (
  event_id INTEGER PRIMARY KEY,
  baker_id INT,
  recipe_id INT,
  bake_date DATE,
  FOREIGN KEY (baker_id) REFERENCES Baker(baker_id),
  FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id)
);
"""
