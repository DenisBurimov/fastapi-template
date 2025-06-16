## Create migrations
```
inv db-migrate --message=001_init
```

## Migrate database
```
inv db-upgrade
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