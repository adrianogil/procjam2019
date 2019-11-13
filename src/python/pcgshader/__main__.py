""" Main entry point of pcgshader module"""
from .grammar import generate as grammar_generate
from .raymarching import generate as generate_raymarching

import sys

if __name__ == "__main__":
    total_run = 1

    if len(sys.argv) > 1:
        total_run = int(sys.argv[1])

    for t in range(0, total_run):
        target_shader = '%s_procedural_shader.frag' % (t,)
        target_file = '%s_shader_image.png' % (t,)

        if '--raymarching' in sys.argv:
            generate_raymarching.generate(target_shader, target_file)
        else:
            grammar_generate.generate(target_shader, target_file)
