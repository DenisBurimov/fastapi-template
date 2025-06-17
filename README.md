## After git clone
```
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Create migrations (if models are changed)
```
inv db-migrate --message=001_init
```

## Migrate database
```
inv db-upgrade
```

## Check the database
```
inv get-users
```

## Run CSS watcher
```
npm run dev:css
```

## Run CSS production build
```
npm run build:css
```

## Make a tailwind archive for offline
```
tar -czf tailwind_toolchain.tgz \
    package.json package-lock.json node_modules \
    app/static/css/src.css \
    tailwind.config.js postcss.config.js
```