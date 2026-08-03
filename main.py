import sys
from config.settings import settings
from core.engine import HuskEngine
from core.memory import ConversationMemory

def main():
    print(f"==================================================")
    print(f"      {settings.HUSK_NAME} AI SYSTEM - TOOL INTEGRATED      ")
    print(f"==================================================")
    print(f"Model: {settings.DEFAULT_MODEL}")
    print(f"Try asking: 'What time is it?' or 'What OS am I on?'")
    print(f"Type 'exit' or 'quit' to end session.\n")

    engine = HuskEngine()
    memory = ConversationMemory(max_history=15)
    memory.load_from_file()

    while True:
        try:
            user_input = input("\nYou > ").strip()
            
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print(f"\nSaving context memory and shutting down {settings.HUSK_NAME}...")
                memory.save_to_file()
                break

            if user_input.lower() == "clear":
                memory.clear()
                print("\n[Memory cleared.]")
                continue

            memory.add_message("user", user_input)

            print(f"{settings.HUSK_NAME} > ", end="", flush=True)

            # Generate response (engine handles tool calls automatically)
            response_text = engine.generate_response(messages=memory.get_messages())

            if response_text:
                print(response_text)
                memory.add_message("assistant", response_text)
                memory.save_to_file()
            else:
                print("\n[Error]: Unable to obtain response.")

        except KeyboardInterrupt:
            print(f"\n\nSaving session and shutting down...")
            memory.save_to_file()
            sys.exit(0)

if __name__ == "__main__":
    main()