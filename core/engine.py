import json
from openai import OpenAI
from config.settings import settings
from modules.tools import AVAILABLE_TOOLS, TOOL_MAP

class HuskEngine:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )
        self.model = settings.DEFAULT_MODEL
        self.system_prompt = (
            f"You are {settings.HUSK_NAME}, an advanced, high-end AI assistant. "
            "You have live access to system information, real-time web search, and web page scraping. "
            "Use search tools whenever asked about real-time events, current data, or recent information."
        )

    def generate_response(self, messages: list):
        full_messages = [{"role": "system", "content": self.system_prompt}] + messages

        try:
            # 1. Initial API Request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                tools=AVAILABLE_TOOLS,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # 2. Handle Tool Call Loop
            if tool_calls:
                full_messages.append(response_message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    
                    if function_name in TOOL_MAP:
                        # Parse argument parameters passed by Gemini
                        raw_args = tool_call.function.arguments
                        kwargs = json.loads(raw_args) if raw_args else {}

                        print(f"\n[Husk Tool Execution]: Running {function_name}({kwargs})...")

                        # Execute local function with unpacked arguments
                        function_to_call = TOOL_MAP[function_name]
                        tool_output = function_to_call(**kwargs)

                        # Append result back to conversation context
                        full_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_output
                        })

                # 3. Second API Request for final answer generation
                second_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=full_messages
                )
                return second_response.choices[0].message.content

            else:
                return response_message.content

        except Exception as e:
            print(f"\n[Engine Error]: Failure during model execution or tool call: {e}")
            return None