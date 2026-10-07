
# # #v1
# import os
# from dotenv import load_dotenv
# from groq import Groq

# # 1. Load credentials securely from .env
# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
# if not api_key:
#     raise RuntimeError("Add GROQ_API_KEY to your .env file")

# # 2. Initialize the official SDK client
# client = Groq(api_key=api_key)
# model = "openai/gpt-oss-20b"

# # 3. Construct the raw JSON message payload
# messages = [
#     {"role": "system", "content": "You are Odyssey, a friendly AI tutor. Explain ideas clearly and simply."},
#     {"role": "user", "content": "Explain what an API is in one simple sentence."},
# ]

# # 4. Invoke the model synchronously
# response = client.chat.completions.create(model=model, messages=messages)
# answer = response.choices[0].message.content
# print(f"Odyssey: {answer}")


# #v2
# import os
# from dotenv import load_dotenv
# from groq import Groq

# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
# if not api_key:
#     raise RuntimeError("Add GROQ_API_KEY to your .env file")

# client = Groq(api_key=api_key)
# model = "openai/gpt-oss-20b"

# print("Odyssey AI is ready. Type 'quit' or 'exit' to leave.")

# # Continuous conversational loop
# while True:
#     prompt = input("\nYou: ").strip()

#     # Handle exit conditions
#     if prompt.lower() in {"quit", "exit"}:
#         print("Odyssey: Until next time!")
#         break

#     # Ignore empty submissions
#     if not prompt:
#         continue

#     # Each turn crafts a fresh request (no memory between turns yet)
#     messages = [
#         {"role": "system", "content": "You are Odyssey, a friendly AI tutor. Explain ideas clearly and simply."},
#         {"role": "user", "content": prompt},
#     ]

#     response = client.chat.completions.create(model=model, messages=messages)
#     answer = response.choices[0].message.content
#     print(f"Odyssey: {answer}")

# #v3
# import os
# import groq
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
# if not api_key:
#     raise RuntimeError("Add GROQ_API_KEY to your .env file")

# client = groq.Groq(api_key=api_key)
# model = "openai/gpt-oss-20b"

# # Maintain state in a manual Python list
# messages = [{"role": "system", "content": "You are Odyssey, a friendly AI tutor. Explain ideas clearly and simply."}]

# print("Odyssey AI is ready. Type 'quit' to leave.")

# while True:
#     try:
#         prompt = input("\nYou: ").strip()
#     except (EOFError, KeyboardInterrupt):
#         print("\nOdyssey: Until next time!")
#         break

#     if prompt.lower() in {"quit", "exit"}:
#         print("Odyssey: Until next time!")
#         break
#     if not prompt:
#         continue

#     # Append user turn to in-memory history
#     messages.append({"role": "user", "content": prompt})

#     try:
#         response = client.chat.completions.create(model=model, messages=messages)
#         answer = response.choices[0].message.content or ""
#         # Append assistant turn so future turns retain context
#         messages.append({"role": "assistant", "content": answer})
#         print(f"Odyssey: {answer}")
#     except groq.RateLimitError:
#         messages.pop()
#         print("Odyssey: The service is busy (Rate Limit). Please wait a moment and retry.")
#     except groq.APIConnectionError:
#         messages.pop()
#         print("Odyssey: Network connection failure. Check your internet connection.")
#     except groq.APIStatusError as error:
#         messages.pop()
#         print(f"Odyssey: API returned HTTP status {error.status_code}. Verify your key and model.")






# # #test with
# # # python -c "from dotenv import load_dotenv; print('dotenv works')"
# #py main.py


# #v4 Langchain Version
# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.messages import HumanMessage, AIMessage

# # 1. Load credentials securely
# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
# if not api_key:
#     raise RuntimeError("Add GROQ_API_KEY to your .env file")

# # 2. Instantiate the Chat Model (Universal interface)
# model = ChatGroq(
#     model="openai/gpt-oss-20b",
#     temperature=0.7,
#     max_tokens=1024,
# )

# # 3. Construct the Composable Prompt Template with Memory Slot
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are Odyssey, a friendly AI tutor. Explain ideas clearly and simply."),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("human", "{question}"),
# ])

# # 4. Instantiate the Typed Output Parser
# parser = StrOutputParser()

# # 5. The LCEL Superpower: Compose the Pipeline using Unix-style Pipes (|)
# # Flow: Dict Input -> Prompt Formatting -> Model Inference -> Clean String Output
# chain = prompt | model | parser

# # 6. Interactive Multi-turn Chat Loop with Token-by-Token Streaming
# chat_history = []
# print("Odyssey AI (LangChain Engine) is ready. Type 'quit' to leave.\n")

# while True:
#     try:
#         user_input = input("You: ").strip()
#     except (EOFError, KeyboardInterrupt):
#         print("\nOdyssey: Until next time!")
#         break

#     if user_input.lower() in {"quit", "exit"}:
#         print("Odyssey: Until next time!")
#         break
#     if not user_input:
#         continue

#     print("Odyssey: ", end="", flush=True)

#     # 7. Real-Time Streaming: tokens yield chunk-by-chunk as generated!
#     response_chunks = []
#     try:
#         for chunk in chain.stream({
#             "chat_history": chat_history,
#             "question": user_input,
#         }):
#             print(chunk, end="", flush=True)
#             response_chunks.append(chunk)
#         print("\n")
#     except Exception as error:
#         print(f"\n[Error communicating with model: {error}]\n")
#         continue

#     # 8. Record turns into typed message objects
#     full_answer = "".join(response_chunks)
#     chat_history.append(HumanMessage(content=user_input))
#     chat_history.append(AIMessage(content=full_answer))



