# Cedar Roasters demo: HTML dashboard behind a login

A practice project for deploying an HTML dashboard on Streamlit Community Cloud
from a **private** GitHub repo, with a **public** app link that requires visitors
to log in or sign up first.

## Folder structure

```
streamlit-demo/
├── app.py                        # Login screen + shows the dashboard
├── requirements.txt              # Python packages
├── .gitignore                    # Keeps secrets out of GitHub
├── dashboard/
│   └── dashboard.html            # The dashboard (replace with yours later)
└── .streamlit/
    ├── config.toml               # Theme colors
    └── secrets.toml.example      # Template for login settings
```

Tip: you can open `dashboard/dashboard.html` directly in your browser to preview it.

---

## 1. Create the private GitHub repo

1. Go to https://github.com/new, name it (e.g. `streamlit-demo`), choose **Private**, and create it.
2. Upload all the files, keeping the folders. On the repo page: **Add file → Upload files**,
   then drag in the whole unzipped folder contents.
   - Hidden folders like `.streamlit` may not show in your file browser. On Mac press
     `Cmd + Shift + .` to show them; on Windows enable "Hidden items" in File Explorer.
   - Do **not** upload a real `secrets.toml`. The `.example` file is fine.

## 2. Set up Auth0 (the account system)

1. Create a free account at https://auth0.com.
2. Go to **Applications → Applications → Create Application**, pick
   **Regular Web Applications**, and create it.
3. In the **Settings** tab, copy the **Domain**, **Client ID** and **Client Secret**.
4. In **Allowed Callback URLs**, add both (comma-separated):
   ```
   http://localhost:8501/oauth2callback, https://YOUR-APP-NAME.streamlit.app/oauth2callback
   ```
   Pick `YOUR-APP-NAME` now; you'll use the same name in step 4. Click **Save**.
5. Sign-up is on by default. To check: **Authentication → Database →
   Username-Password-Authentication**, and make sure **Disable Sign Ups** is off.
6. Optional: under **Authentication → Social**, enable Google so users can
   "Continue with Google". (Auth0's built-in Google keys are fine for testing;
   add your own Google keys before real use.)

## 3. Prepare your secrets

1. Generate a cookie secret:
   ```
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. Copy `.streamlit/secrets.toml.example`, fill in your values, and keep it handy.
   You'll paste it into Streamlit Cloud.

## 4. Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub.
2. When asked, **allow access to private repositories** (or later: your avatar →
   Settings → Linked accounts → GitHub). Otherwise your private repo won't be listed.
3. Click **Create app → Deploy a public app from GitHub**.
4. Choose your repo, branch `main`, main file `app.py`, and set the
   **App URL** to `YOUR-APP-NAME` (same as in Auth0).
5. Open **Advanced settings → Secrets** and paste your filled-in secrets, with:
   ```
   redirect_uri = "https://YOUR-APP-NAME.streamlit.app/oauth2callback"
   ```
6. Click **Deploy** and wait a minute or two.

## 5. Make the app public (repo stays private)

Apps from private repos start as private. In your app: **⋮ → Settings → Sharing →
Who can view this app → "This app is public and searchable"**. Save.

Now open the link in a private/incognito window to test as a new visitor:
welcome screen → **Log in / Sign up** → create an account → dashboard.

---

## Optional: run it on your computer first

```
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then fill it in
streamlit run app.py
```
Keep `redirect_uri = "http://localhost:8501/oauth2callback"` for local testing.

## Swapping in your real dashboard

1. Replace `dashboard/dashboard.html` with your file (keep the name, or change
   `DASHBOARD_FILE` in `app.py`).
2. If your HTML loads local CSS/JS/images by relative path (e.g. `style.css`),
   paste them into the HTML file instead. Linked local files don't load inside Streamlit.
3. If the dashboard is cut off, raise `DASHBOARD_HEIGHT` in `app.py`.
4. Commit to GitHub. Streamlit redeploys automatically.

## Troubleshooting

- **"Login isn't configured yet"**: the `[auth]` section is missing from secrets.
- **Auth0 says "Callback URL mismatch"**: the `redirect_uri` in secrets must exactly
  match one of the Allowed Callback URLs in Auth0 (including `https` and `/oauth2callback`).
- **Logging out then straight back in without a password**: Streamlit's logout clears
  the app's session but Auth0 remembers the browser. Use incognito to test as a new user.
- **Repo not listed when deploying**: grant Streamlit access to private repos (step 4.2).
