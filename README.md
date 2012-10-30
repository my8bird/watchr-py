# INSTALL
git clone git@github.com:my8bird/watchr-py.git
cd watchr-py
python setup.py install

# Usage
```python
import watchr
# Watch all python file changes under this directory
monitor = watchr.watch('.*\.py')
monitor.all.on(handleAllChanges)
# monitor.created
# monitor.deleted
# monitor.modified
# monitor.moved
```

# Additional args for `watchr.watch`

