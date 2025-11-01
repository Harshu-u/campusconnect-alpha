Local HTTPS options when Chrome forces HTTPS

This document explains a few practical options so you can open your development site with HTTPS (useful when Chrome auto-upgrades to https:// or HSTS blocks HTTP).

Option A — Preferred: Use `django-extensions` (runserver_plus) + mkcert (serves HTTPS locally on 127.0.0.1)

1. Install `django-extensions` and supporting packages in your venv (done in this repo):

   pip install django-extensions pyOpenSSL werkzeug

2. Install mkcert (https://mkcert.dev/) on your machine and add it to trust store:
   - Windows (using chocolatey): `choco install mkcert` then `mkcert -install`.
   - Or follow mkcert site instructions for your OS.

3. Create cert and key for localhost in the project root (run from project folder):

   mkcert -key-file devkey.pem -cert-file devcert.pem 127.0.0.1 localhost ::1

   This creates `devcert.pem` and `devkey.pem`.

4. Combine key+cert into a single PEM (required by `runserver_plus`):

   On Windows (CMD):
   ```cmd
   type devkey.pem devcert.pem > devcombined.pem
   ```

   On PowerShell:
   ```powershell
   Get-Content devkey.pem,devcert.pem | Out-File -Encoding ascii devcombined.pem -Force
   ```

5. Run Django with HTTPS using `runserver_plus`:

   ```bash
   python manage.py runserver_plus 127.0.0.1:8000 --cert-file devcombined.pem
   ```

   Because you used mkcert and installed its CA into your OS/browser trust store, Chrome will trust the certificate and you can open https://127.0.0.1:8000.

Option B — Quick alternative: Use ngrok (no project config changes)
1. Install ngrok (https://ngrok.com/) and login.
2. Run your dev server normally:

   python manage.py runserver 127.0.0.1:8000

3. In another terminal run ngrok:

   ngrok http 8000

4. ngrok will show a public HTTPS URL (e.g. https://abcd1234.ngrok.io). Open that URL in Chrome — it will be HTTPS and tunnel to your local server.

Option C — Browser workaround (not recommended long-term)
- Clear HSTS for localhost in Chrome (temporary): open `chrome://net-internals/#hsts` and in "Delete domain security policies" enter `127.0.0.1` and click Delete. Also delete `localhost` entry if present. Restart Chrome.
- Alternatively, open an incognito window and try `http://127.0.0.1:8000`.

Notes & troubleshooting
- If you still get "site can’t be reached" on https://127.0.0.1:8000 it is because the dev server is not serving TLS. Use Option A or B above.
- If you use mkcert ensure the certificate file names you pass to runsslserver match the files you created.
- When done with local HTTPS for development, you can remove `devcert.pem` and `devkey.pem` if desired.

Security
- Do NOT use self-signed or mkcert certs in production. Use a proper CA and production-ready WSGI/ASGI server + reverse proxy (e.g., gunicorn+nginx or uvicorn/nginx).

If you want, I can:
- Generate a small script/Makefile to run mkcert and start runsslserver for you.
- Or configure a simple `run_https_dev.bat` (Windows) that runs mkcert (if available) and starts the server.
