from jinja2 import Environment, BaseLoader
from docx import Document
from src.llm import LLM

report_generator_prompt = open("src/agents/report_generator/prompt.jinja2").read().strip()

class ReportGenerator:
    def __init__(self, base_model, api_key):
        self.llm = LLM(base_model, api_key)

    def render(self, prompt):
        env = Environment(loader=BaseLoader())
        template = env.from_string(report_generator_prompt)

        return template.render(prompt=prompt)

    def validate_response(self, response: str) -> bool:
        return True
    def parse_response(self, response: str):
        result = {"project": "", "focus": "", "plans": {}, "summary": ""}

        reply = ""
        current_section = None
        current_step = None

        for line in response.split("\n"):
            line = line.strip()

            if line.startswith("Project Name:"):
                current_section = "project"
                result["project"] = line.split(":", 1)[1].strip()
            elif line.startswith("Your Reply to the Human Prompter:"):
                reply = line.split(":", 1)[1].strip()
            elif line.startswith("Current Focus:"):
                current_section = "focus"
                result["focus"] = line.split(":", 1)[1].strip()
            elif line.startswith("Plan:"):
                current_section = "plans"
            elif line.startswith("Summary:"):
                current_section = "summary"
                result["summary"] = line.split(":", 1)[1].strip()
            elif current_section == "reply":
                result["reply"] += " " + line
            elif current_section == "focus":
                result["focus"] += " " + line
            elif current_section == "plans":
                if line.startswith("- [ ] Step"):
                    current_step = line.split(":")[0].strip().split(" ")[-1]
                    result["plans"][int(current_step)] = line.split(":", 1)[1].strip()
                elif current_step:
                    result["plans"][int(current_step)] += " " + line
            elif current_section == "summary":
                result["summary"] += " " + line.replace("```", "")

        result["project"] = result["project"].strip()
        result["focus"] = result["focus"].strip()
        result["summary"] = result["summary"].strip()

        return reply, result

    def execute(self, prompt: str) -> str:
        prompt = self.render(prompt)
        response = self.llm.inference(prompt)
        return response
    
    def generate_report(self, response, filename):
    # Check if filename ends with .docx, if not, append it
        if not filename.endswith('.docx'):
            filename += '.docx'

        # Create a new Document
        doc = Document()
        doc.add_heading('Report Template', level=1)

        # Add the response as a paragraph
        doc.add_paragraph(response)

        # Save the document
        doc.save(filename)
        print(f'Report template created: {filename}')