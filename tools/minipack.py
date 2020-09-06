from __future__ import print_function

def run():
    from os.path import join, split, splitext, isdir, isfile, basename, dirname
    from os import listdir, walk, stat
    from shutil import copy, copytree
    
    import menutils

    try:
        from python_minifier import minify
    except ImportError:
        menutils.clear_screen()
        print("Required package 'python-minifier' is not installed.")
        menutils.e_pause()
        return

    PYPACKS_DIR = join("..", "Monika After Story", "game", "python-packages")
    options = [("Python Package/Module Minifier", "Package/Module: ")]

    original_size = 0
    minified_size = 0

    for path in listdir(PYPACKS_DIR):
        path = join(PYPACKS_DIR, path)
        if isfile(path) and splitext(path)[1] == ".py":
            options.append(("Module " + basename(path), path))
        elif isdir(path) and not splitext(path)[1] == ".dist-info" and "__pycache__" not in path:
            options.append(("Package " + basename(path), path))

    path = 1
    while path is not None:
        path = menutils.menu(options)
        if path is None:
            break

        if isfile(path):
            files = [splitext(path)[0] + "_min.py"]
            copy(path, files[0])
        else:
            minipack_dir = path + "_min"
            copytree(path, minipack_dir)
            files = []
            for dir_, _, walk_files in walk(minipack_dir):
                for file_ in walk_files:
                    if splitext(file_)[1] != ".py":
                        continue
                    files.append(join(dir_, file_))
        
        menutils.clear_screen()
        for file_ in files:
            print("Working on " + basename(file_))
            src = ""
            fd = open(file_, "r")
            try:
                while True:
                    chunk = fd.read(8192)
                    if not chunk:
                        break
                    src += chunk
                    original_size += len(chunk)
            finally:
                fd.close()
            
            minified = minify(src)
            fd = open(file_, "w")
            try:
                while minified:
                    chunk = minified[:8192]
                    fd.write(chunk)
                    minified = minified[8192:]
                    minified_size += len(chunk)
            finally:
                fd.close()
        print("Minified size: " + str(minified_size) + " bytes")
        print("Original size: " + str(original_size) + " bytes")
        print("Minification rate: " + "{:.2f}%".format(float(minified_size) / original_size * 100))

        if not menutils.ask("Minify another package"):
            break
