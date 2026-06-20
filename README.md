# Spanish to English Streamlit Translator

This app uses the existing local Gemma4 endpoint from `test_request.py`:

```text
http://0.0.0.0:8000/chat/local_llm/
```

It accepts Spanish `.txt`, `.md`, `.docx`, and `.pdf` files, extracts their text, sends it to the model in chunks, and saves an English `.txt` translation under `translations/`.

## Run

```bash
conda activate trnsf
cd /home/cvpro/code_files/translate
python app.py
```

Running `python app.py` starts Streamlit on port `8550` and opens Windows Edge at:

```text
http://127.0.0.1:8550
```

Keep the Gemma4 service running before you translate. You can edit the endpoint in the app if the service is exposed at a different host or port.
