from llm import llm
from langchain.agents import AgentExecutor, create_tool_calling_agent
from tools.question_tool import QuestionsTool
from tools.codegen_tool import CodeGenTool
from langchain_core.prompts import ChatPromptTemplate

user_input = "Create a dashboard showing sales analysis over inventory"

schema = """
Table: src.products
Columns: id, cost, category, name, brand, retail_price, department, sku, distribution_center_id

Table: src.inventory_items
Columns: id, product_id, created_at, sold_at, cost, product_category, product_name, product_brand, product_retail_price,
 product_department, product_sku, product_distribution_center_id

Table: src.orders
Columns: order_id, user_id, status, gender, created_at, returned_at, shipped_at, delivered_at, num_of_item
#status: Complete, Processing, Shipped, Returned, Cancelled

Table: src.order_items
Columns: id, order_id, user_id, product_id, inventory_item_id, status, created_at, shipped_at, delivered_at, 
returned_at, sale_price

Table: distribution_centres
Columns: id, name, latitude, longitude, distribution_center_geom
"""

tools = [QuestionsTool, CodeGenTool]

input = {"prompt": user_input, "dbschema": schema}

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Data Analyst who can generate code and answer analytics questions"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               verbose=True,
                               return_intermediate_steps=True)

output = agent_executor.invoke({'input': input})

for i in output['intermediate_steps']:
    print(i[0].tool)
    
output['intermediate_steps']