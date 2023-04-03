echo Syncing main to pypi package
rsync -a --delete main.py packages/pypi/src/Raindrop_metalfoxdev/main.py
echo Sync Finished
