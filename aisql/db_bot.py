import json
from openai import OpenAI
import os
import sqlite3
from time import time

from build import main as build_db
from schema import (
    sql_create_baker_table,
    sql_create_recipe_table,
    sql_create_ingredient_table,
    sql_create_recipeIngredient_table,
    sql_create_category_table,
    sql_create_recipeCategory_table,
    sql_create_review_table,
    sql_create_bakeEvent_table,
)

print("Running db_bot.py!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# SQLITE
sqliteDbPath = getPath("baking.sqlite") 

# remove existing db before
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

# build the DB fresh each run so the data is consistent
# this calls your build.py which creates tables and inserts rows
build_db()

# open a connection
sqliteCon = sqlite3.connect(sqliteDbPath)
sqliteCon.row_factory = sqlite3.Row
sqliteCursor = sqliteCon.cursor()

def runSql(query):
    q = query.strip()
    if not q.lower().startswith("select"):
        raise ValueError("Only SELECT statements are allowed.")
    cur = sqliteCon.execute(q)
    cols = [d[0] for d in cur.description] if cur.description else []
    return [dict(zip(cols, row)) for row in cur.fetchall()]

# Build a CREATE TABLE script string for prompt context
setupSqlScript = "\n".join([
    "PRAGMA foreign_keys = ON;",
    sql_create_baker_table.strip(),
    sql_create_recipe_table.strip(),
    sql_create_ingredient_table.strip(),
    sql_create_recipeIngredient_table.strip(),
    sql_create_category_table.strip(),
    sql_create_recipeCategory_table.strip(),
    sql_create_review_table.strip(),
    sql_create_bakeEvent_table.strip(),
])

# OPENAI
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(api_key=config["openaiKey"])
openAiClient.models.list()  

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o",  # or "gpt-4o-mini"
        messages=[{"role": "user", "content": content}],
        stream=True,
    )
    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)
    result = "".join(responseList)
    return result

# strategies
commonSqlOnlyRequest = (
    " Give me a sqlite select statement that answers the question. "
    "Only respond with sqlite syntax. If there is an error do not explain it!"
)

# in-domain demo that matches your schema (Ingredient+RecipeIngredient+Recipe)
single_domain_demo_q = "Which ingredients and amounts are used in Chocolate Cake?"
single_domain_demo_sql = (
    " \nSELECT i.name, ri.amount\n"
    "FROM Ingredient i\n"
    "JOIN RecipeIngredient ri ON i.ingredient_id = ri.ingredient_id\n"
    "JOIN Recipe r ON r.recipe_id = ri.recipe_id\n"
    "WHERE r.name = 'Chocolate Cake';\n "
)

strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (
        setupSqlScript
        + " " + single_domain_demo_q
        + single_domain_demo_sql
        + commonSqlOnlyRequest
    ),
}

# bakery questions to demo
questions = [
    "Which baker made each recipe?",
    "Which recipes take more than 60 minutes to bake?",
    "Average rating by recipe.",
    "Which ingredients and amounts are used in Banana Muffins?",
    "Which bakers are Experts and how many recipes have they made?",
    "Show all reviews for Chocolate Cake.",
    "How many recipes are there per difficulty level?",
    "Which bakers have made at least 2 recipes?",
    "Which recipes were baked on 2025-09-27?",
    "Which ingredients are not used by any recipe?",
]

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]
    return value.strip()

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    print("########################################################################")
    print(f"Running strategy: {strategy}")
    for question in questions:

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Question:")
        print(question)
        error = "None"
        sqlSyntaxResponse = ""
        queryRawResponse = ""
        friendlyResponse = ""
        try:
            getSqlFromQuestionEngineeredPrompt = strategies[strategy] + " " + question
            sqlSyntaxResponse = getChatGptResponse(getSqlFromQuestionEngineeredPrompt)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print("SQL Syntax Response:")
            print(sqlSyntaxResponse)

            rows = runSql(sqlSyntaxResponse)
            queryRawResponse = json.dumps(rows, indent=2)
            print("Query Raw Response:")
            print(queryRawResponse)

            friendlyResultsPrompt = (
                'I asked a question: "' + question + '" and I queried this database '
                + setupSqlScript + " with this query " + sqlSyntaxResponse
                + '. The query returned the results data: "' + queryRawResponse
                + '". Could you concisely answer my question using the results data?'
            )
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print("Friendly Response:")
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{int(time())}.json"), "w") as outFile:
        json.dump(responses, outFile, indent=2)

sqliteCursor.close()
sqliteCon.close()
print("Done!")
