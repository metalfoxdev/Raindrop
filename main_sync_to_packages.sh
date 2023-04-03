echo Syncing main to pypi package
rsync -a --delete main.py packages/pypi/src/Raindrop/main.py
echo Sync Finished
