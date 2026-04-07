from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
import os

load_dotenv()

# đọc system prompt
with open("system_prompt", "r", encoding="utf-8") as f:
    system_prompt = f.read()


# định nghĩa agentstate
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# Khởi tạo LLM với Tools
tools = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
)
llm_and_tools = llm.bind_tools(tools)


# Agent Node
def agent_node(state: State):
    massage = state["messages"]
    # kiểm tra câu đầu tiên trong hội thoại có phải hệ thống không
    if not isinstance(massage[0], SystemMessage):
        message = [SystemMessage(content=system_prompt)] + massage

    response = llm_and_tools.invoke(message)

    # LOGGING
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Tool Call: {tc['name']}{tc['args']}")
    else:
        print("Trả lời trực tiếp")
    return {"messages": [response]}


# xây dựng Graph
def create_travel_agent():
    builder = StateGraph(State)

    # Khai báo node agent
    builder.add_node("agent", agent_node)

    # Khai báo node tools chung cho tất cả các tools
    tool_node = ToolNode(tools)
    builder.add_node("tools", tool_node)

    # Khai báo edges
    builder.add_edge(START, "agent")

    # Điều kiện rẽ nhánh (nếu có tool call thì sang node tools, nếu không thì kết thúc END)
    builder.add_conditional_edges("agent", tools_condition)

    # Sau khi chạy tools xong, quay lại agent để suy luận tiếp
    builder.add_edge("tools", "agent")

    return builder.compile()


# Chat loop
if __name__ == "__main__":
    agent = create_travel_agent()
    print("Travel Agent: Xin chào! Tôi là trợ lý du lịch TravelBuddy. Bạn muốn đi đâu?")
    print("Gõ 'quit' để thoát")
    print("=" * 50)
    while True:
        user_input = input("Bạn: ").strip()
        if user_input.lower() == "quit":
            break
        print("\nTravelBuddy đang suy nghĩ...")
        response = agent.invoke({"messages": [("human", user_input)]})
        print("TravelBuddy:", response["messages"][-1].content)
        print("=" * 50)
