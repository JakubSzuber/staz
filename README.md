# Setup

Remember to set up ".env" file in those directories:
- **staz/api_container** - OPENAI_API (OpenAI key), LOCAL_HOME (path in local machine where the WSL is mounted e.g. "/run/desktop/mnt/host/c/Users/jszub" if you uses Windows), API_KEY_1, API_KEY_2, API_KEY_3 (API keys that can be used outside to communicate to FastAPI container)
- **staz/my_tennis_club/members** - FASTAPI_KEY (of the FastAPI's keys like e.g. value of API_KEY_1)
- **staz/my_tennis_club/my_tennis_club** - POSTGRES_PASS (password to PostgreSQL container)

Commands to execute compose:
- `cd staz/my_tennis_club`
- `docker compose --env-file ../api_container/.env up -d --build`

Furthermore, my_tennis_club-web-1 container among others on initial execution requires `python manage.py migrate`.


TODO enhance readme and repo name, tags, ect
