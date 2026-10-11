# Prompt Injection in Translation

This app uses the local Gemma4 endpoint from `gemma-main.py`:


<img src="https://github.com/computervisionpro/prompt-injection/tree/main/assets/translate-img.png" alt="Translation" width="600" height="370">



LM-Studio quantized models:
https://lmstudio.ai/models/gemma-4

```text
http://0.0.0.0:8000/chat/local_llm/
```

It accepts Spanish `.txt`, `.md`, `.docx`, and `.pdf` files, extracts their text, sends it to the model in chunks, and saves an English `.txt` translation under `translations/`.

## Run

```bash
conda activate <your_env>
python gemma-main.py
python app.py
```

Running `python app.py` starts Streamlit on port `8550` and opens Edge browser at:

```text
http://127.0.0.1:8550
```

Keep the Gemma4 service running before you translate. You can also edit the endpoint in the app if the service is exposed at a different host or port. The system prompt can be edited in `app.py` file line number 157.


Once you run the model, you can drop one of the text files available in the `assets` folder. One file contains a prompt injection text. When you drop the injected file and if the system prompt is weak, for eg. "Translate this Spanish document chunk to English.", then it will perform the injected task instead of translation.

However, if you use a strong Instructional prompt like "You are a professional translator. Translate Spanish text into natural English. Preserve paragraph breaks, names, numbers, lists, and document meaning. Return only the English translation." then it won't get injected.
