from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder,PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from tools import search_tool,wiki_tool,save_tool
import os

load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object= ResearchResponse)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert research assistant tasked with writing high-quality, comprehensive research papers.\n\n"
            "When a user asks a query, follow these steps strictly:\n"
            "1. Use the Search tool to gather deep, actual real-world facts, population figures, and demographics.\n"
            "2. Combine those findings into a highly detailed, multi-line report. Use headings (e.g., 'Key Statistics:', 'Demographics:') and bullet points.\n"
            "3. CRITICAL: Replace all placeholders, brackets, or template markers with the actual numbers and text you found during your search. Do not write text like '[insert number]'—type out the true data (e.g., 'Total population: 700,000,000').\n"
            "4. Pass this fully populated, multi-line report string into the 'save_text_to_file' tool.\n"
            "5. Finally, return the exact same report string as your final response so the compiler can structure it."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [search_tool,wiki_tool,save_tool]
# 1. Bind your tools directly to the model instance
llm_with_tools = llm.bind_tools(tools)

agent = prompt | llm_with_tools

agent = create_tool_calling_agent(

    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True )



# --- 1. Define the formatting prompt ---
formatting_prompt = ChatPromptTemplate.from_template(
    "You are a data formatting specialist.\n"
    "Take the following text and format it precisely according to the structural instructions.\n"
    "Text to format:\n{text}\n\n"
    "{format_instructions}"
)

formatted_chain = formatting_prompt.partial(format_instructions=parser.get_format_instructions()) | llm | parser


if __name__ == "__main__":
    query = input("what can i help you research? ")
    try:
        raw_response = agent_executor.invoke({"query": query, "chat_history": []})
        agent_output_text = raw_response.get("output", "")
        print(agent_output_text)
    except Exception as e:
        print(f"\nAn error occurred during terminal execution: {e}")
    
