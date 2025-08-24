from typing import Optional, List, TypedDict
from langgraph.graph import StateGraph, END
from helpers import select_target_from_messages, extract_user_last_message, extract_system_last_message, build_prompt_messages
from retriever import retrieve_context
from llm_provider import generate_chat_completion


class GraphState(TypedDict):
    messages: List[dict]
    target: Optional[str]


PERSONAS = ["pablo", "ramiro"]


def router(state: GraphState) -> GraphState:
    if not state.get("target"):
        detected = select_target_from_messages(state.get("messages", []), PERSONAS)
        state["target"] = detected or PERSONAS[0]

    # Extraer el prompt del usuario
    user_messages = [m for m in state["messages"] if m.get("role") == "user"]
    if user_messages:
        prompt = user_messages[-1]["content"]
        context = retrieve_context(state["target"], prompt)
        # Inyectar como mensaje de sistema o campo adicional
        state["messages"].insert(0, {
            "role": "system",
            "content": "\n".join(context)
        })

    return state



def agent_factory(nombre: str):
    def agent(state: GraphState) -> GraphState:
        # 1) Tomamos la pregunta original del usuario
        user_text = extract_user_last_message(state.get("messages", [])) or ""

        # 2) Recuperamos contexto del state en vez de buscar de nuevo.
        raw_context = extract_system_last_message(state["messages"])
        context_chunks = raw_context.split("\n") if raw_context else []

        # 3) Construimos el prompt y llamamos al LLM
        prompt_msgs = build_prompt_messages(nombre, user_text, context_chunks)
        try:
            answer = generate_chat_completion(prompt_msgs)
        except Exception as e:
            answer = (
                f"No pude generar una respuesta automática en este momento. "
                f"(Motivo: {e}). Contexto recuperado:\n- " + "\n- ".join(context_chunks[:3])
            )

        # 4) Registramos la respuesta del agente en el historial
        state["messages"].append({"role": "assistant", "content": answer, "name": f"agent_{nombre}"})
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