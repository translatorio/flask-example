"""A locale file translator on the Translatorio Python SDK, in Flask."""

import base64
import math
import os
from pathlib import Path

from flask import Flask, render_template, request
from translatorio import (
    AuthenticationError,
    Client,
    InvalidRequest,
    QuotaExhausted,
    RateLimited,
    ServerError,
    TranslatorioError,
)
from werkzeug.exceptions import RequestEntityTooLarge

LANGUAGES = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt-BR": "Portuguese (Brazil)",
    "ja": "Japanese",
}
SAMPLE = Path(__file__).parent / "samples" / "en.json"
NO_KEY = "TRANSLATORIO_KEY is not set. Start the app with your key: TRANSLATORIO_KEY=tr_test_... flask --app app run"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # 1 MB for the whole upload

key = os.environ.get("TRANSLATORIO_KEY", "")
tr = Client(
    key,
    base_url=os.environ.get("TRANSLATORIO_URL") or "https://translatorio.com/api",
) if key else None


@app.get("/")
def form():
    """The form, with the sample file and Spanish ticked."""
    return page(200 if tr else 500, error=None if tr else NO_KEY)


@app.post("/translate")
def translate():
    """Send the file to Translatorio and show one translated file per language."""
    chosen = request.form.getlist("targets")
    form = {
        "targets": [code for code in LANGUAGES if code in chosen],  # only the languages offered
        "context": request.form.get("context", "").strip(),
        "sample": "sample" in request.form,
    }
    upload = request.files.get("file")

    if tr is None:
        return page(500, **form, error=NO_KEY)

    if upload and upload.filename:
        filename, content = upload.filename, upload.read()  # the bytes as they are
    elif form["sample"]:
        filename, content = SAMPLE.name, SAMPLE.read_bytes()
    else:
        return page(422, **form, error="Choose a file, or tick Use the sample file.")

    if not form["targets"]:
        return page(422, **form, error="Pick at least one language to translate into.")

    fields = []

    try:
        result = tr.translate_file(content, form["targets"], filename=filename, context=form["context"] or None)
    except AuthenticationError:
        error = "Translatorio did not accept the key. Check TRANSLATORIO_KEY."
    except QuotaExhausted as e:
        left = f" {e.remaining:,} left." if "credits" in e.payload else ""
        error = f"Not enough credits to translate this file.{left}"
    except InvalidRequest as e:
        error = e.message
        fields = [message for messages in e.fields.values() for message in messages if message != e.message]
    except RateLimited as e:
        error = f"Too many requests. Try again in {math.ceil(e.retry_after)} seconds."
    except ServerError as e:
        error = "Could not reach Translatorio. Try again in a moment." if e.status == 0 else e.message
    except TranslatorioError as e:
        error = e.message
    else:
        return page(200, **form, result=result)

    return page(422, **form, error=error, fields=fields)


@app.errorhandler(RequestEntityTooLarge)
def too_large(_):
    """Over MAX_CONTENT_LENGTH: the form again, saying why, rather than a bare 413."""
    return page(413, error="The file is over 1 MB, the most this example takes.")


@app.template_filter("base64")
def to_base64(text: str) -> str:
    """A translated file as base64, for the data: URI of its Download link."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def page(status: int, **values):
    """The page, with the form as it was sent and whatever came back."""
    values = {"targets": ["es"], "context": "", "sample": True, **values}
    return render_template("translator.html", languages=LANGUAGES, **values), status
