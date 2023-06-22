# Setup

Remember to set up ".env" file with the PostgreSQL password in the same directory as "settings.py" and another ".env" within "api_container" directory that will contain OPENAI_API (API key for OpenAI) and LOCAL_HOME (path in local machine where the WSL is mounted e.g. "/run/desktop/mnt/host/c/Users/jszub" if you uses Windows).

Commands to execute compose:
- `cd staz/my_tennis_club`
- `docker compose --env-file ../api_container/.env up -d --build`

Furthermore, my_tennis_club-web-1 container among others on initial execution requires `python manage.py migrate`.
