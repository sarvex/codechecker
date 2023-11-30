# -------------------------------------------------------------------------
#
#  Part of the CodeChecker project, under the Apache License v2.0 with
#  LLVM Exceptions. See LICENSE for license information.
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# -------------------------------------------------------------------------

import glob
import os


def _generate_func_map_lines(func_map_dir):
    """ Iterate over all lines of input files in random order. """
    files = glob.glob(os.path.join(func_map_dir, '*'))
    for func_map_file in files:
        with open(func_map_file, 'r',
                          encoding='utf-8', errors="ignore") as func_map:
            yield from func_map


def _create_global_ctu_function_map(func_map_lines):
    """ Takes iterator of individual function maps and creates a global map.

    It will keeping only unique names. We leave conflicting names out of CTU.
    A function map contains the id of a function (mangled name) and the
    originating source (the corresponding AST file) name.
    """
    mangled_to_asts = {}

    # We collect all occurences of a function name into a set.
    for line in func_map_lines:
        line = line.strip()
        # FIXME: Detect and report invalid input.
        # The format of the external function map file changed in between
        # clang-15 and clang-16, check whether this is the updated format.
        # The new file format is <Length>:<USR> <File-Path>
        if line[0].isdigit():
            length_str, _ = line.split(':', 1)
            length = int(length_str)
            sep_pos = len(length_str) + 1 + length
            mangled_name = line[:sep_pos]
            ast_file = line[sep_pos + 1:]  # Skipping the ' ' separator
        else:  # The old file format
            mangled_name, ast_file = line.split(' ', 1)
        if mangled_name not in mangled_to_asts:
            mangled_to_asts[mangled_name] = {ast_file}
        else:
            mangled_to_asts[mangled_name].add(ast_file)

    return [
        (mangled_name, ast_files.pop())
        for mangled_name, ast_files in mangled_to_asts.items()
        if len(ast_files) == 1
    ]


def merge(func_map_dir, output_file):
    """ Merge individual function maps into a global one.

    As the collect phase runs parallel on multiple threads, all compilation
    units are separately mapped into a temporary file in ctu_temp_fnmap_folder.
    These function maps contain the mangled names of functions and the source
    (AST generated from the source) which had them.
    These files should be merged at the end into a global map file:
    ctu_func_map_file.
    """
    func_map_lines = _generate_func_map_lines(func_map_dir)
    mangled_ast_pairs = _create_global_ctu_function_map(func_map_lines)

    # Write (mangled function name, ast file) pairs into final file.
    with open(output_file, 'w',
              encoding='utf-8', errors='ignore') as out_file:
        for mangled_name, ast_file in mangled_ast_pairs:
            out_file.write('%s %s\n' % (mangled_name, ast_file))
