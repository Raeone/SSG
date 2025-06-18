import os
import shutil

def copy_all_content(src, dst):
  if not os.path.exists(src):
    raise Exception(f"Folder {src} does not exist")  
  
  if not os.path.exists(dst):
    os.mkdir(dst)
    
  print(f"..Starting copying from {src} to {dst}")

  items = os.listdir(src) # [file, dir, ...] obsah src slozky
  print(f"...{src} contains: {items}")

  for item in items:
    item_path = os.path.join(src, item)
    item_dst_path = os.path.join(dst, item)

    if os.path.isfile(item_path):      
      shutil.copy(item_path, dst)
      print(f"..Copying {item_path} to {dst}")
    else:
      print(f"...{item} is directory with {item_path} path")            
      copy_all_content(item_path, item_dst_path)
      