import os
import shutil

def clear(folderpath: str, debug: bool=False):
  """
  Eliminates every file from a folder.
  """

  for filename in os.listdir(folderpath):
    file_path = os.path.join(folderpath, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)  # Remove files or symlinks
        if debug:
          print(f"removed {file_path}")
      elif os.path.isdir(file_path):
        shutil.rmtree(file_path)  # Remove subdirectories
        if debug:
          print(f"removed {file_path}")
    except Exception as e:
        print(f'Failed to delete {file_path}. Reason: {e}')
def makeDir(folder: str, existing:bool=True):
  """
  Makes a directory.
  """
  os.makedirs(folder,exist_ok=existing)