rsync -r -t --exclude='obj' --exclude='.mypy_cache' --exclude='__pycache__' --delete -a --info=progress2 ~/Dropbox/prog/Stocks charm@virtual:/home/charm
#ssh charm@virtual "cd Stocks && ./run.sh"
