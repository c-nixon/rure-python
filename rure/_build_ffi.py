import os

from cffi import FFI

ffi = FFI()

cur_dir = os.path.dirname(os.path.abspath(__file__))
header_dir = os.path.join(cur_dir, "..", "include")
header_fname = os.path.join(header_dir, "rure.h")
header_lines = open(header_fname).readlines()

target_dir = os.getenv("CARGO_TARGET_DIR")

if target_dir:
    if not os.path.isabs(target_dir):
        target_dir = cur_dir + "/../" + target_dir

    extra_objects = [os.path.sep.join((root, f))
                     for root, dirs, files in os.walk(target_dir)
                     for f in files
                     if (f == "librure.a" and
                     root.split(os.sep)[-1] == "release")]

    if len(extra_objects) == 1:
        ffi.set_source('rure._ffi',
                """#include "rure.h" """,
                include_dirs=[header_dir],
                extra_objects=extra_objects)
    else:
        ffi.set_source('rure._ffi', None)
else:
    ffi.set_source('rure._ffi', None)

header = []

for line in header_lines:
    # Strip lines known to break cdef
    if line.startswith(('}\n', '#ifdef', 'extern "C"', '#ifndef',
                        '#endif', '#define', '#include')):
        continue
    else:
        header.append(line)

ffi.cdef('\n'.join(header))

if __name__ == '__main__':
    ffi.compile(verbose=True)
