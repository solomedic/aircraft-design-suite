# Aircraft Design Toolbox

This repository contains the Streamlit app for the Aircraft Design Toolbox based on Nicolai, Raymer, and Sadraey methods.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
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

If you want to connect this workspace to the target repository, use:

```bash
git init
git remote add origin https://github.com/solomedic/aircraft-design-suite.git
```
