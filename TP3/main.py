from pearson_graph import GraphState, app

state: GraphState = {"messages": [], "target": "juan"}
final = app.invoke(state)
print(final["messages"])
# [{'role': 'assistant', 'content': 'Respuesta de juan'}]
