# aircraft-design-suite

Aircraft Design Toolbox based on Nicolai Design Book is developed in this repository. It is a working development repo for the Streamlit-based aircraft design suite.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

If you want to run the tests locally, install the dev dependency as well:

```bash
python -m pip install -r requirements-dev.txt
pytest
```

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from the GitHub repo.
3. Set the main file path to `app.py`.
4. Confirm the required packages are installed from `requirements.txt`.

## After Hosting

1. Verify the app opens without dependency errors.
2. Confirm the images load correctly from the repository root.
3. If you update the app, push to GitHub again and let Streamlit redeploy automatically.

## GitHub remote

The repository is configured for:

```bash
https://github.com/solomedic/aircraft-design-suite.git
```
