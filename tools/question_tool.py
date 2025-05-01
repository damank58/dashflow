import json
from llm import llm
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
# Tool: Generate Questions and Suggested Chart Types


class QuestionGenerationInput(BaseModel):
    prompt: str = Field(..., description="User Request")
    db_schema: str = Field(..., description="The database schema including table and column definitions.")


def generate_questions_and_chart(prompt: str, db_schema: str) -> str:
    instruction = f"""
    You are a data analyst tasked with designing a dashboard based on the user's request.
    Your goal is to generate most insightful and diverse analytical questions that will guide the dashboard design.

    Based on the following user prompt,
    - Suggest one appropriate title for the dashboard with Word limit of 6-7 words.
    - Generate 6 relevant questions a data analyst might ask.
    - Use given database schema to generate these questions logically. Do not include information which cannot be answered.
    
    For each question, 
    - Suggest a suitable chart type to visualize the answer (e.g., bar chart, line chart, pie chart).
    - An appropriate header for that chart.
    
    Also, write 2 questions that would generate metrics / indicator only.
    - Give Chart Type as Indicator
    - One or two words header for this chart.
    
    Output only in JSON format, with keys 'dashboard_title'and 'questions' where:
    - The 'dashboard_title' key comprises of one value that is the title for the dashboard.
    - The questions key should further have keys 'question', 'chart_type' and 'chart_header'.

    user_prompt: {prompt}
    Database Schema: {db_schema}
    """
    response = llm.invoke(instruction).content
    output = response.strip("```json").strip("```")
    try:
        return json.dumps(json.loads(output), indent=2)
    except Exception as err:
        raise Exception('Value is incorrect. {}'.format(err))
    # fallback in case model returns non-JSON


QuestionsTool = StructuredTool(
    name="questions_generator",
    func=generate_questions_and_chart,
    description="Useful in generating analysis questions and recommended chart types based on a user prompt.",
    args_schema=QuestionGenerationInput
)

