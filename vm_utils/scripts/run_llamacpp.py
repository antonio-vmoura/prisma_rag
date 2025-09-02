from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.core.llms import ChatMessage, MessageRole

def messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        if message.role == 'system':
            prompt += f"\n{message.content}</s>\n"
        elif message.role == 'user':
            prompt += f"\n{message.content}</s>\n"
        elif message.role == 'assistant':
            prompt += f"\n{message.content}</s>\n"

    # ensure we start with a system prompt, insert blank if needed
    if not prompt.startswith("\n"):
        prompt = "\n</s>\n" + prompt

    # add final assistant prompt
    prompt = prompt + "\n"

    return prompt

def completion_to_prompt(completion):
    return f"\n</s>\n\n{completion}</s>\n\n"

model_path = "./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

settings_kwargs = {
    "tfs_z": 1.0,
    "top_k": 40,
    "top_p": 1.0,
    "repeat_penalty": 1.1, 
    "n_gpu_layers": -1,
    "offload_kqv": True,
}

llm = LlamaCPP(
    model_path=model_path,
    temperature=0.1,
    max_new_tokens=512,
    context_window=3900,
    generate_kwargs={},
    # All to GPU
    model_kwargs=settings_kwargs,
    # transform inputs into Llama2 format
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=False,
)

# Formulate a question as a user message
question_message = ChatMessage(content="Me conte uma piada em português", role=MessageRole.USER)

# Use the message to prompt the model
response = llm.chat(messages=[question_message])

# Print the response
print(str(response))
