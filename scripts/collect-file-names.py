import os
import glob
from typing import List
import yaml

MMTK_DEV = os.path.dirname(os.path.realpath(__file__))
MMTK_CORE = f'{MMTK_DEV}/mmtk-core'
MMTK_OPENJDK = f'{MMTK_DEV}/mmtk-openjdk'

def cleanup_paths(paths: List[str]):
    paths = [p.replace('/home/wenyuz/MMTk-Dev/','')  for p in paths]
    paths.sort()
    return paths


mmtk_core_files = cleanup_paths([
    *glob.glob(f'{MMTK_CORE}/src/**/*.rs', recursive=True),
    *glob.glob(f'{MMTK_CORE}/Cargo.lock', recursive=True),
    *glob.glob(f'{MMTK_CORE}/Cargo.toml', recursive=True),
])

rust_binding_files = cleanup_paths([
    *glob.glob(f'{MMTK_OPENJDK}/mmtk/src/**/*.rs', recursive=True),
    *glob.glob(f'{MMTK_OPENJDK}/mmtk/Cargo.lock', recursive=True),
    *glob.glob(f'{MMTK_OPENJDK}/mmtk/Cargo.toml', recursive=True),
])

cpp_binding_files = cleanup_paths([
    *glob.glob(f'{MMTK_OPENJDK}/openjdk/**/*.h', recursive=True),
    *glob.glob(f'{MMTK_OPENJDK}/openjdk/**/*.hpp', recursive=True),
    *glob.glob(f'{MMTK_OPENJDK}/openjdk/**/*.cpp', recursive=True),
    *glob.glob(f'{MMTK_OPENJDK}/openjdk/**/*.gmk', recursive=True),
])

all_files = {
    'mmtk-core-files': mmtk_core_files,
    'mmtk-openjdk-rust-files': rust_binding_files,
    'mmtk-openjdk-cpp-files': cpp_binding_files,
}

with open(r'files.yml', 'w') as file:
    # yaml.dump(all_files, file)
    stream = yaml.dump(all_files, default_flow_style = False)
    text = stream \
        .replace('\n- ', '\n  - ') \
        .replace('mmtk-core-files:', '# Rust source files in mmtk-core for generating mmtk-openjdk.so\nmmtk-core-files:') \
        .replace('mmtk-openjdk-rust-files:', '# Rust source files in mmtk-openjdk for generating mmtk-openjdk.so\nmmtk-openjdk-rust-files:') \
        .replace('mmtk-openjdk-cpp-files:', '# C++ source files in mmtk-openjdk. Not included in mmtk-openjdk.so but is used for connecting to the .so file\nmmtk-openjdk-cpp-files:')
    file.write(text)
