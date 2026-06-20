
# conda install -c nvidia cuda-toolkit=12.4.1
# CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python
# CMAKE_ARGS="-DGGML_CUDA=on -DGGML_CUDA_FA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
# export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH

import asyncio, copy
from pydantic import BaseModel
from fastapi import FastAPI
from typing import List, Dict
from llama_cpp import Llama
from contextlib import asynccontextmanager




MAX_TOKENS = 3700


class RequestSchema(BaseModel):
    req_id: str
    query: List[Dict[str, str]]

class ResponseSchema(BaseModel):
    req_id: str
    response: str
    success: bool


@asynccontextmanager
# it will execute the code before the yield, 
# and after exiting, it will execute the code after the yield
async def lifespan(app: FastAPI):
    print("\nLoading model...")

    app.state.llm = Llama(
        model_path="gemma-4-E2B-it-Q4_K_M.gguf",
        n_ctx=4096,
        n_gpu_layers=-1,
        flash_attn=True,
        verbose=False
    )

    print("Model loaded\n\n")

    yield  # app runs here

    # (optional cleanup)
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

def check_tokens(history, llm):
    print(history)

    while True:
        
        # [{'role': 'system', 'content': 'You are a polite assistant, helping people answer their questions. 
        # Keep your answer always within 200 words only.'}, {'role': 'user', 'content': 'Tell me about xyz'}]
        total_tokens = sum(len(llm.tokenize(f'{msg["role"]}: {msg["content"]}'.encode("utf-8"))) 
                               for msg in history )
        
        if total_tokens <= MAX_TOKENS:
            return True
        
        else:
            # if more convo than the first question
            if len(history) > 2:
                # popping second oldest term because at 0 there is system prompt
                history.pop(1)
            else:
                # 1st question itself has too many tokens
                return False

model_lock = asyncio.Lock()
# semaphore = asyncio.Semaphore(2)  # allow 2 requests

# while True:
@app.post("/chat/local_llm/", response_model=ResponseSchema)
async def bot(request: RequestSchema):

    try:

        # Use the lock so multiple requests don't crash the VRAM
        async with model_lock:

            llm = app.state.llm
            # Event loops run asynchronous tasks
            loop = asyncio.get_running_loop()
            
            req_id = request.req_id
            history = copy.deepcopy(request.query)

            valid_tokens = check_tokens(history, llm)


            if valid_tokens:
                output = await asyncio.wait_for(loop.run_in_executor(
                            None, lambda: llm.create_chat_completion(
                            messages=history,
                            max_tokens=400,
                            temperature=0.2 #.7, stream=True
                                                            )), 60)

                response = output["choices"][0]["message"]["content"]
                print(f"\n\nGemma: {response}\n")

                return {"req_id": req_id, "response": response, "success": True}
            else:
                return {"req_id": req_id, "response": "Your question exceeds the token limit !", "success": False}

    except Exception as e:
        print("\nClosing the chat. BYE !")
        print(e)
        return ResponseSchema(
            req_id=request.req_id,
            response="Sorry, I encountered an internal error.",
            success=False
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# https://huggingface.co/google/gemma-4-E4B-it
# https://lmstudio.ai/models/google/gemma-4-e4b
# https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
