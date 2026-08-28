from strands import Agent
from strands.models.ollama import OllamaModel


# Connect to Ollama
model = OllamaModel(
    model_id="minimax-m3:cloud",
    host="http://127.0.0.1:11434"
)


# Create the AI agent
agent = Agent(
    model=model,
    system_prompt="You are a helpful AI assistant. Chat with the user in a friendly way."
)


# Chat loop
while True:
    user_input = input("\nUser: ")

    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye! 👋")
        break

    agent(user_input)