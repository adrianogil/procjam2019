""" Module responsible for generating shaders using simple grammar"""
from simplegrammar import SimpleGrammar
from pcgshader.glslviewer import GlslViewer


def generate(target_shader, target_file):
    """
        generate
    """
    shader = SimpleGrammar() \
        .set_text("#main_structure#")\
        .add_tag("main_structure", [
            """
uniform float u_time;
uniform vec2 u_mouse;
uniform vec2 u_resolution;

void main (void) {
    gl_FragColor = vec4(0.01, 0.01, 0.01, 1.0);
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    vec3 color = vec3(0.0, 0.0, 0.0);
    vec3 color1 = vec3(0.0, 0.0, 0.0);
    vec3 color2 = vec3(0.0, 0.0, 0.0);

    #shader_code#

    color = normalize(color);
    color = abs(color);

    gl_FragColor.xyz = color;
}
            """
        ])\
        .add_tag("shader_code", [
            """
            #uv_based_code_structure#
            #uv_based_code_structure#
            #uv_based_code_structure#
            """,
            """
            #uv_based_code_structure#
            #uv_based_code_structure#
            #uv_based_code_structure#
            #uv_based_code_structure#
            """,
            """
            #uv_based_code_structure#
            #uv_based_code_structure#
            #uv_based_code_structure#
            #uv_based_code_structure#
            #uv_based_code_structure#
            """,
        ])\
        .add_tag("uv_based_code_structure", [
            """
if (#uv_based_condition#)
{
    #uv_based_code#
} else {
    #uv_based_code#
}
            """,
            """
for(int i=0; i<#random_int#; i++)
{
    #uv_based_code#
}
            """,
            """
#uv_based_code#
#st_transformation#
#uv_based_code#
            """,
            """
#uv_based_code#
color1 = color;
#st_transformation#
#uv_based_code#
color2 = color;
#st_transformation#
#uv_based_code#
color = 0.333 * (color + color1 + color2);
            """,
            """
#uv_based_code#
color1 = color;
#st_transformation#
#uv_based_code#
color = smoothstep(length(color), length(color1), #uv_based_value#) * color;
            """,
        ])\
        .add_tag("uv_based_code", [
            """
color += vec3(#random_number#, #random_number#, #random_number#);
            """,
            """
color += vec3(#uv_based_value#, #uv_based_value#, #uv_based_value#);
            """,
            """
color = vec3(abs(color.x - #uv_based_value#), abs(color.y - #uv_based_value#), abs(color.z - #uv_based_value#));
            """,


            """
color += vec3(#uv_based_value#, #uv_based_value#, #uv_based_value#);
            """,
            """
color.x += #uv_based_value#;
            """,
            """
color.y += #uv_based_value#;
            """,
            """
color.z += #uv_based_value#;
            """
        ])\
        .add_tag("uv_based_value", [
            "#random_number# + #uv_based_value#",
            "#uv_based_value# * sign(#uv_based_value#)",
            "smoothstep(#random_number#, #random_number#, #uv_based_value#)",
            "smoothstep(#uv_based_value#, #uv_based_value#, #uv_based_value#)",
            "abs(st.x - #random_number#) - abs(st.y - #random_number#)",
            "abs(st.x - #random_number#) + abs(st.y - #random_number#)",
            "abs(st.x - #random_number#) * abs(st.y - #random_number#)",
            "abs(st.x - #uv_based_value#) + abs(st.y - #uv_based_value#)",
            "abs(st.x - #uv_based_value#) * abs(st.y - #uv_based_value#)",
            "dot(st, vec2(0.5, 0.5))",
            "length(st - vec2(#random_number#, #random_number#))",
            "length(st - vec2(#uv_based_value#, #uv_based_value#))",
            "length(vec2(#uv_based_value#, #uv_based_value#) - vec2(#random_number#, #random_number#))",
            "#random_number# * max(st.x, st.y)",
            "#random_number# * max(#uv_based_value#, #uv_based_value#)",
            "#random_number# * st.x",
            "#random_number# * st.y",
            "#random_number# * st.x + #random_number# * st.y",
            "#random_number# * sin(#uv_based_value#)",
        ])\
        .add_tag("uv_based_condition", [
            "#uv_based_value# > #random_number#",
            "#uv_based_value# < #random_number#",
            "#uv_based_value# > #random_number# && #uv_based_value# < #random_number#",
            "abs(#uv_based_value# - #random_number#) < #random_number#",
        ])\
        .add_tag("st_transformation", [
            "st.xy = fract(st * 10.0);",
            "st.xy = #random_number# * st.yx;",
            "st.xy = st.xy - vec2(0.5, 0.5);",
            "st.xy = st.xy - vec2(#random_number#, #random_number#);",
            "st.xy = vec2(#random_number#, #random_number#) * vec2(st.x + st.y, st.x * st.y);",
            "st.xy = vec2(sin(#random_number# * st.x), cos(#random_number# * st.y));",
        ])\
        .add_tag("random_number", [
            "0.1", "-0.3", "0.4", "0.01", "0.77", "0.14", "0.00001", "0.5", "0.99", "0.25", "0.83"
        ])\
        .add_tag("random_medium_number", [
            "2.0", "2.5", "5.0", "7.5", "10.0"
        ])\
        .add_tag("random_int", [
            "2", "5", "6", "7", "10", "20"
        ])

    shader = """
#ifdef GL_ES
precision mediump float;
#endif
    """ + str(shader)

    print("Shader generated by simple grammar:\n%s" % (shader,))

    shader_path = target_shader

    with open(shader_path, 'w') as shader_file:
        shader_file.write(str(shader))

    shader_viewer = GlslViewer(shader_path, {
        'output': target_file,
        # 'headless': True,
        'verbose': True,
        'size': 500,
        'extra_arguments': '-s 5'
    })
    shader_viewer.run()
    # shader_viewer.start()
    # shader_viewer.stop()
