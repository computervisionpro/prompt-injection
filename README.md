# Spanish to English Translator

This app uses the local Gemma4 endpoint from `gemma-main.py`:

LM-Studio quantized models:
https://lmstudio.ai/models/gemma-4

```text
http://0.0.0.0:8000/chat/local_llm/
```

It accepts Spanish `.txt`, `.md`, `.docx`, and `.pdf` files, extracts their text, sends it to the model in chunks, and saves an English `.txt` translation under `translations/`.

## Run

```bash
conda activate trnsf
python gemma-main.py
python app.py
```

Running `python app.py` starts Streamlit on port `8550` and opens Edge browser at:

```text
http://127.0.0.1:8550
```

Keep the Gemma4 service running before you translate. You can also edit the endpoint in the app if the service is exposed at a different host or port.
