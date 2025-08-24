from dotenv import load_dotenv
load_dotenv(override=False)
from pearson_graph import GraphState, app

state: GraphState = {"messages": [{"role": "user", "content": "¿Ramiro puede programar en Python?"}]}
final = app.invoke(state)
print(final["messages"])
