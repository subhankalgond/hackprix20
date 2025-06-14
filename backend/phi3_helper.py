from llama_cpp import Llama

# Path to your downloaded model
model_path = "C:\\llm\\models\\phi-3-mini-4k-instruct.Q4_K_M.gguf"

# Load the model
llm = Llama(model_path=model_path, n_ctx=4096)

def get_ai_response(prompt):
    response = llm(
        prompt=f"<|user|>\n{prompt}\n<|assistant|>",
        temperature=0.7,
        top_p=0.9,
        max_tokens=512,
        stop=["<|user|>", "<|assistant|>"],
    )
    return response["choices"][0]["text"].strip()
