import json
from llm import llm
from tools.codegen_tool import CodeGenTool
from tools.question_tool import QuestionsTool
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from py_file import generate_streamlit_script


class DashAgent(object):
    def __init__(self, schema):
        self.schema = schema
        pass

    def graph_agent(self, user_prompt: str):
        input = json.dumps({"prompt": user_prompt, "dbschema": self.schema})

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a Data Analyst who can generate code and answer analytics questions"),
                ("human", "{messages}"),
                ("placeholder", "{agent_scratchpad}")
            ]
        )
        tools = [QuestionsTool, CodeGenTool]

        langgraph_agent_executor = create_react_agent(llm, tools, prompt=prompt)

        messages = langgraph_agent_executor.invoke({"messages": [("human", input)]})
        output = messages['messages']
        return output

    def create_dashboard(self, user_prompt, no_of_col=3):
        output = self.graph_agent(user_prompt)

        page_code = []
        dashboard_title = ''
        questions = []
        code_ls = []
        function_name = []

        for i in range(len(output) - 1):
            if output[i].content.strip():
                if 'dashboard_title' in output[i].content.strip('[]'):
                    title = json.loads(output[i].content.strip())['dashboard_title'].replace(" ", "_")
                    dashboard_title = f'{title.replace("_", " ")}'
                if 'streamlit_code' in output[i].content.strip('[]'):
                    questions.append(json.loads(output[i].content.strip('[]'))['question'])
                    function_name.append(json.loads(output[i].content.strip('[]'))['function_name'])
                    code_ls.append(json.loads(output[i].content.strip('[]'))['streamlit_code'])

                    page_code.append({
                        'dashboard_title': dashboard_title,
                        'question': json.loads(output[i].content.strip('[]'))['question'],
                        'function_name': json.loads(output[i].content.strip('[]'))['function_name'],
                        'code_ls': json.loads(output[i].content.strip('[]'))['streamlit_code'],
                        'chart_type': json.loads(output[i].content.strip('[]'))['chart_type']
                    })

        generate_streamlit_script(filename=dashboard_title, columns=no_of_col, page_code=page_code)

