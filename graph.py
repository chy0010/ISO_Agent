from typing import Annotated, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import AnyMessage, SystemMessage
from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
import grid_rag
import miso_tools
import spp_tools
import eia_tools
 
load_dotenv()
 
 
@tool
def miso_fuel_mix():
    """MISO current fuel mix (real-time) — MW and % by source."""
    return miso_tools.get_fuel_mix()
 
@tool
def miso_load():
    """MISO current system load (real-time), in MW."""
    return miso_tools.get_load()
 
@tool
def miso_prices(location: str = None):
    """MISO real-time electricity prices (LMP, $/MWh) by location.
    Pass a location like 'INDIANA' to filter."""
    return miso_tools.get_lmp(location=location)
 
@tool
def spp_fuel_mix():
    """SPP current fuel mix (real-time) — MW and % by source. SPP is wind-heavy."""
    return spp_tools.get_fuel_mix()
 
@tool
def spp_load():
    """SPP current system load (real-time), in MW."""
    return spp_tools.get_load()
 
@tool
def spp_prices(location: str = None):
    """SPP real-time electricity prices (LMP, $/MWh) at hubs.
    Pass 'NORTH' or 'SOUTH' to filter."""
    return spp_tools.get_lmp(location=location)
 
@tool
def eia_fuel_mix(iso: str):
    """Fuel mix for any US grid via EIA (hourly, ~1-2h lag). No prices.
    Use for PJM, ERCOT, CAISO, NYISO, ISONE, or MISO/SPP fallback.
    iso: one of MISO, PJM, SPP, CAISO, ERCOT, NYISO, ISONE."""
    return eia_tools.get_fuel_mix(iso)
 
@tool
def eia_load(iso: str):
    """System load for any US grid via EIA (hourly, ~1-2h lag).
    iso: one of MISO, PJM, SPP, CAISO, ERCOT, NYISO, ISONE."""
    return eia_tools.get_load(iso)

@tool
def explain_grid_concept(question: str):
    """Explain grid concepts, terminology, and market rules — what LMP means,
    why prices differ by location, why fuel mix changes, what congestion is,
    and MISO settlement/tariff/business-practice rules. Use this for
    'why'/'what does X mean' questions, requests about practices, rules, or
    procedures, or to add context to a data answer. Returns passages from
    grid market documentation."""
    return grid_rag.retrieve(question)
 
 
tools = [
    miso_fuel_mix, miso_load, miso_prices,
    spp_fuel_mix, spp_load, spp_prices,
    eia_fuel_mix, eia_load,
    explain_grid_concept
]


SYSTEM = """You are a US electric grid assistant answering questions from live data tools.

Sources:
- MISO and SPP: native tools (real-time, includes prices).
- Other grids (PJM, ERCOT, CAISO, NYISO, ISONE): EIA tools (fuel mix + load only, no prices).
- Comparisons: use EIA for all grids involved so numbers are comparable.
- For "why" or "what does X mean" questions, call explain_grid_concept and cite the source.
Always report the timestampit .Answer "why" questions in 1-2 sentences with the actual reason, not a breakdown of every component. If two values are nearly identical, just say so."""

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

llm = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

def call_model(state: AgentState) -> AgentState:
    return {"messages": [llm.invoke(state["messages"])]}

def should_continue(state:AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("model", call_model)
graph.add_node("tools", ToolNode(tools))

graph.add_conditional_edges(
    "model",
    should_continue,
    {
        "continue":"tools",
        "end":END
    }
)
graph.add_edge(START, "model") 
graph.add_edge("tools", "model")                      

checkpointer = InMemorySaver()
app = graph.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "session-1"}}
    app.invoke({"messages": [SystemMessage(content=SYSTEM)]}, config=config)  # seed ONCE
    while True:
        q = input("\nIf you have any grid question please ask ?: ")
        if q.lower() in ("quit", "exit", "no"):
            break

        final = None
        for chunk in app.stream({"messages": [("user", q)]}, config=config):
            for node_name, node_output in chunk.items():
                msg = node_output["messages"][-1]
                if getattr(msg, "tool_calls", None):
                    for tc in msg.tool_calls:
                        args = tc["args"] or {}
                        arg_str = ", ".join(f"{k}={v}" for k, v in args.items())
                        print(f"  calling tool :  {tc['name']}")
                final = msg

        print("\n" + final.content)