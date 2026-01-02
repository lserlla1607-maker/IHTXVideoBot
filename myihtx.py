import subprocess
import shlex
import os
filename = input("file name?")
command = input("command?")
time = input("time?")
powers = int(input("powers?"))
def run(i,co,o):
  try:
    subprocess.run(shlex.split(f"ffmpeg -i {i} {co} -t {time} {o}"),check=True,capture_output=True)
  except Exception as e:
    print(str(e))
run(filename,command,"1.ts")
def concat(items):
  conc = "|".join(items)
  try:
    subprocess.run(shlex.split(f'ffmpeg -i "concat:{conc}" ihtx_custom.mp4'),check=True,capture_output=True)
  except Exception as e:
    print(str(e))
files = []
for i in range(powers):
  files.append(f"{i+1}.ts")
print(files)
for i, v in enumerate(files):
  run(v,command,f"{i+2}.ts")
concat(files)
for i in range(powers+1):
  if os.path.exists(f"{i+1}.ts"):
    os.remove(f"{i+1}.ts")
print("> ⚠️ Warning: Make sure you ~~die~~ `.t sync+` this")