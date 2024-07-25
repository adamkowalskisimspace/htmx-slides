shell:
  poetry shell

setup:
  poetry install
  npm install

dev:
  poetry run fastapi dev main.py --host 0.0.0.0 --port 8080

tw:
  npx tailwind -i ./style.css -o static/style.css --watch
