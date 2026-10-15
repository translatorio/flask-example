![Translatorio Flask example](https://raw.githubusercontent.com/translatorio/flask-example/main/art/banner.png)

# Translatorio example: Flask

A locale file translator built with [Translatorio](https://translatorio.com), Flask and the Python SDK ([translatorio/python-sdk](https://github.com/translatorio/python-sdk)). Upload a translation file (JSON, PO, XLIFF, CSV, Android XML, iOS `.strings`, Markdown, HTML or plain text), or use the sample, pick the languages, and get one file back per language with the same keys and structure. Placeholders such as `{name}`, `%(name)s` and `%d`, and links, are kept away from the model and put back as they were, and each file says whether all of them came back. Every file shows a preview and downloads from the page.

The file goes up as it is and nothing is kept: no database and nothing written to disk, so the call to Translatorio is the only code worth reading.

The walkthrough is on the blog: [translatorio.com/blog/translate-locale-files-in-flask](https://translatorio.com/blog/translate-locale-files-in-flask).

## Run it

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
TRANSLATORIO_KEY=tr_test_... flask --app app run --port 8000
```

The translation is in [`app.py`](app.py). Requires Python 3.9 or later.

## What you need

- A Translatorio key from [your keys](https://translatorio.com/organization/keys). The free
  plan is enough: 2,000 credits a month. A `tr_test_` key is free and never reaches the
  model: its translations come back marked, like `[es] Hello`. Use a live key to see real
  translations.

It goes in the environment as `TRANSLATORIO_KEY`. `TRANSLATORIO_URL` is optional: the API's
address, `https://translatorio.com/api` unless you set it.

## The other examples

The same app with each client: [plain PHP](https://github.com/translatorio/php-example), [Laravel](https://github.com/translatorio/laravel-example), [Express](https://github.com/translatorio/express-example) and [Flask](https://github.com/translatorio/flask-example).

## Author

Created by [Edu Lazaro](https://edulazaro.com) for [Translatorio](https://translatorio.com), the translation API it shows.

## License

This example is open-sourced software licensed under the [MIT license](LICENSE).
