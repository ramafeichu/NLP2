from typing import Optional, List, TypedDict
from langgraph.graph import StateGraph, END
from helpers import _select_target_from_messages

class GraphState(TypedDict):
    messages: List[dict]
    target: Optional[str]


PERSONAS = ["ana", "juan"]


def router(state: GraphState) -> GraphState:
    if not state.get("target"):
        detected = _select_target_from_messages(state.get("messages", []), PERSONAS)
        if detected in PERSONAS:
            state["target"] = detected
    return state


def agent_factory(nombre: str):
    def agent(state: GraphState) -> GraphState:
        state["messages"].append({"role": "assistant", "content": f"Respuesta de {nombre}"})
        return state
    return agent


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("router", router)

    for p in PERSONAS:
        graph.add_node(f"agent_{p}", agent_factory(p))
    
    graph.set_entry_point("router")

    def route_edge(state: GraphState) -> str:
        target = state.get("target")
        if target in PERSONAS:
            return f"agent_{target}"
        return f"agent_{PERSONAS[0]}"
    
    possible_targets = [f"agent_{p}" for p in PERSONAS]
    graph.add_conditional_edges("router", route_edge, possible_targets)

    for p in PERSONAS:
        graph.add_edge(f"agent_{p}", END)

    return graph.compile()



app = build_graph()