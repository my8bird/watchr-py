import re

from watchdog.events import FileSystemEvent

# Module under test
import sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root)
from watchr import FSEventWatcher

def assert_signal_emitted(eventHandler, signal, fileEvent):
   called = []
   def sigHandler(*args, **kwds):
      called.append((args, kwds))

   signal.on(sigHandler)
   eventHandler(fileEvent)
   signal.off(sigHandler)

   assert len(called) > 0, 'Signal not emitted'

def assert_signal_not_emitted(eventHandler, signal, fileEvent):
   called = []
   def sigHandler(*args, **kwds):
      called.append((args, kwds))

   signal.on(sigHandler)
   eventHandler(fileEvent)
   signal.off(sigHandler)

   assert len(called) == 0, 'Signal emitted'


class Test_FSEventWatcher(object):
   def test_catchAll(self):
      # Given: A watcher that handles all events
      watcher = FSEventWatcher()

      # Then: All events are progated
      event = FileSystemEvent('created', '/home/something', is_directory = True)
      assert_signal_emitted(watcher.on_created, watcher.created, event)
      event = FileSystemEvent('created', '/home/something', is_directory = False)
      assert_signal_emitted(watcher.on_created, watcher.created, event)

      event = FileSystemEvent('moved', '/home/something', is_directory = True)
      assert_signal_emitted(watcher.on_moved, watcher.moved, event)
      event = FileSystemEvent('moved', '/home/something', is_directory = False)
      assert_signal_emitted(watcher.on_moved, watcher.moved, event)

      event = FileSystemEvent('modified', '/home/something', is_directory = True)
      assert_signal_emitted(watcher.on_modified, watcher.modified, event)
      event = FileSystemEvent('modified', '/home/something', is_directory = False)
      assert_signal_emitted(watcher.on_modified, watcher.modified, event)

      event = FileSystemEvent('deleted', '/home/something', is_directory = True)
      assert_signal_emitted(watcher.on_deleted, watcher.deleted, event)
      event = FileSystemEvent('deleted', '/home/something', is_directory = False)
      assert_signal_emitted(watcher.on_deleted, watcher.deleted, event)

   def test_onlyFiles(self):
      # Given: A watcher that handles only file events
      watcher = FSEventWatcher(allowDirs = False)

      # Then: Only file events
      event = FileSystemEvent('created', '/home/something', is_directory = True)
      assert_signal_not_emitted(watcher.on_created, watcher.created, event)
      event = FileSystemEvent('created', '/home/something', is_directory = False)
      assert_signal_emitted(watcher.on_created, watcher.created, event)

      event = FileSystemEvent('moved', '/home/something', is_directory = True)
      assert_signal_not_emitted(watcher.on_moved, watcher.moved, event)
      event = FileSystemEvent('moved', '/home/something', is_directory = False)
      assert_signal_emitted(watcher.on_moved, watcher.moved, event)

      event = FileSystemEvent('modified', '/home/something', is_directory = True)
      assert_signal_not_emitted(watcher.on_modified, watcher.modified, event)
      event = FileSystemEvent('modified', '/home/something', is_directory = False)
      assert_signal_emitted(watcher.on_modified, watcher.modified, event)

      event = FileSystemEvent('deleted', '/home/something', is_directory = True)
      assert_signal_not_emitted(watcher.on_deleted, watcher.deleted, event)
      event = FileSystemEvent('deleted', '/home/something', is_directory = False)
      assert_signal_emitted(watcher.on_deleted, watcher.deleted, event)

   def test_onlyDirs(self):
      # Given: A watcher that handles only directoryevents
      watcher = FSEventWatcher(allowFiles = False)

      # Then: Only directory events
      event = FileSystemEvent('created', '/home/something', is_directory = True)
      assert_signal_emitted(watcher.on_created, watcher.created, event)
      event = FileSystemEvent('created', '/home/something', is_directory = False)
      assert_signal_not_emitted(watcher.on_created, watcher.created, event)

      event = FileSystemEvent('moved', '/home/something', is_directory = True)
      assert_signal_emitted(watcher.on_moved, watcher.moved, event)
      event = FileSystemEvent('moved', '/home/something', is_directory = False)
      assert_signal_not_emitted(watcher.on_moved, watcher.moved, event)

      event = FileSystemEvent('modified', '/home/something', is_directory = True)
      assert_signal_emitted(watcher.on_modified, watcher.modified, event)
      event = FileSystemEvent('modified', '/home/something', is_directory = False)
      assert_signal_not_emitted(watcher.on_modified, watcher.modified, event)

      event = FileSystemEvent('deleted', '/home/something', is_directory = True)
      assert_signal_emitted(watcher.on_deleted, watcher.deleted, event)
      event = FileSystemEvent('deleted', '/home/something', is_directory = False)
      assert_signal_not_emitted(watcher.on_deleted, watcher.deleted, event)

   def test_regex_preCompiled(self):
      # Given: A watcher that handles only directoryevents
      watcher = FSEventWatcher(re.compile('.*match.*'))

      # Then: Only paths which 
      event = FileSystemEvent('created', '/nope', is_directory = True)
      assert_signal_not_emitted(watcher.on_created, watcher.created, event)

      event = FileSystemEvent('created', '/match', is_directory = True)
      assert_signal_emitted(watcher.on_created, watcher.created, event)
      event = FileSystemEvent('created', '/home/match/other', is_directory = True)
      assert_signal_emitted(watcher.on_created, watcher.created, event)

   def test_regex(self):
      # Given: A watcher that handles only directoryevents
      watcher = FSEventWatcher('.*match.*')

      # Then: Only paths which match
      event = FileSystemEvent('created', '/nope', is_directory = True)
      assert_signal_not_emitted(watcher.on_created, watcher.created, event)

      event = FileSystemEvent('created', '/match', is_directory = True)
      assert_signal_emitted(watcher.on_created, watcher.created, event)
      event = FileSystemEvent('created', '/home/match/other', is_directory = True)
      assert_signal_emitted(watcher.on_created, watcher.created, event)
