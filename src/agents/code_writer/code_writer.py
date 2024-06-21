from jinja2 import Environment, BaseLoader

from src.llm import LLM

coder_prompt = open("src/agents/code_writer/prompt.jinja2").read().strip()

class CodeWriter:
    def __init__(self, base_model, api_key):
        self.llm = LLM(base_model, api_key)

    def render(self, plan, prompt):
        env = Environment(loader=BaseLoader())
        template = env.from_string(coder_prompt)
        return template.render(
            step_by_step_plan=plan,
            user_prompt=prompt,
        )
    
    def validate_response(self, response):
        response = response.strip()

        response = response.split("~~~", 1)[1]
        response = response[: response.rfind("~~~")]
        response = response.strip()

        result = []
        current_file = None
        current_code = []
        code_block = False

        for line in response.split("\n"):
            if line.startswith("File: "):
                if current_file and current_code:
                    result.append(
                        {"file": current_file, "code": "\n".join(current_code)}
                    )
                current_file = line.split("`")[1].strip()
                current_code = []
                code_block = False

            elif line.startswith("```"):
                current_code.append(line)
                code_block = not code_block
            else:
                current_code.append(line)

        if current_file and current_code:
            code = "\n".join(current_code)
            code += "```"

            result.append({"file": current_file, "code": code})

        return result

    def execute(self, step_by_step_plan: str, user_prompt: str):
        prompt = self.render(step_by_step_plan,user_prompt)
        response = self.llm.inference(prompt)
        print(response)
        valid_response = self.validate_response(response)

        while not valid_response:
            print("Invalid response from the assistant, trying again...")
            return self.execute(step_by_step_plan, user_prompt)
        return valid_response