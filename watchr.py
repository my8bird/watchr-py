import re

from watchdog.observers import Observer
from watchdog.events    import FileSystemEventHandler

RegexObject = re.compile('')

def watch(matcher = None, path = '.', recursive = False, allowFiles = True, allowDirs = True):
   handler = FSEventWatcher(matcher    = matcher,
                            allowFiles = allowFiles,
                            allowDirs  = allowDirs)

   observer = Observer()
   observer.schedule(handler, path = path, recursive = recursive)
   observer.start()
   return handler


class FSEventWatcher(FileSystemEventHandler):
   def __init__(self, matcher=None, allowFiles=True, allowDirs=True):
      # If the matcher is set but is not a compiled regular expression then
      # compile it to speed things up for each file change.
      if matcher is not None and not type(matcher) is RegexObject:
         matcher = re.compile(matcher)

      # Store the file matching fields
      self._allowFiles = allowFiles
      self._allowDirs  = allowDirs
      self._matcher = matcher

      # Create the signals we can emit
      self.all      = Signal()
      self.created  = Signal()
      self.deleted  = Signal()
      self.modified = Signal()
      self.moved    = Signal()

   def on_created(self, event):
      self._handle(self.created, event)

   def on_deleted(self, event):
      self._handle(self.deleted, event)

   def on_modified(self, event):
      self._handle(self.modified, event)

   def on_moved(self, event):
      self._handle(self.moved, event)

   def _handle(self, signal, event):
      if self._shouldNotify(event):
         signal.emit(event.src_path,
                     isdir  = event.is_directory,
                     isfile = not event.is_directory)

   def _shouldNotify(self, event):
      matches_type = (self._allowFiles and not event.is_directory) or \
                     (self._allowDirs and event.is_directory)

      if not matches_type:
         return False

      return self._matcher is None or self._matcher.match(event.src_path) is not None


class Signal(object):
   def __init__(self):
      self._handlers = []

   def on(self, handler, *args, **kwds):
      self._handlers.append((handler, (args, kwds)))

   def off(self, handler, *args, **kwds):
      self._handlers.remove((handler, (args, kwds)))

   def emit(self, *args, **kwds):
      # Find handlers to apply
      handlers = [h for h, config in self._handlers if self._shouldApply(config, args, kwds)]

      # Call each handler
      return [h(*args, **kwds) for h in handlers]

   def _shouldApply(self, (hArgs, hKwds), emitArgs, emitKwds):
      if len(hArgs) > len(emitArgs):
         # The signal has less arguments then the handler so they can not match
         return False

      for i, arg in enumerate(hArgs):
         if arg != emitArgs[i]:
            # A positional argument did not match
            return False

      for key, value in hKwds.viewitems():
         # If signal does not have a required key or the values do not match
         if not emitKwds.has_key(key) or value != emitKwds[key]:
            return False

      return True
