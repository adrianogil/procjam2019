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
distance = #raymarch_object#;

#shader_code#
            """
        ])\
        .add_tag("shader_code", [
            """
            distance = min(distance, #raymarch_object#);
            """,
            """
            distance = min(distance, #raymarch_object#);
            distance = min(distance, #raymarch_object#);
            distance = min(distance, #raymarch_object#);
            """,
            """
            distance = min(distance, #raymarch_object#);
            distance = min(distance, #raymarch_object#);
            distance = min(distance, #raymarch_object#);
            distance = min(distance, #raymarch_object#);
            """,
        ])\
        .add_tag("raymarch_object", [
            """
sdSphere(p, vec3(#random_number#, #random_number#, #random_number#), #random_number#)
            """,
            """
udBox(p, vec3(#random_number#, #random_number#, #random_number#), vec3(#random_number#, #random_number#, #random_number#))
            """,
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

uniform float u_time;
uniform vec2 u_mouse;
uniform vec2 u_resolution;

// Based on code from https://gist.github.com/sephirot47/f942b8c252eb7d1b7311

// these constants are used throughout the shader,
// they can be altered to avoid glitches or optimize the framerate,
// their meaning can best be seen in context below
#define NEAR_CLIPPING_PLANE 0.1
#define FAR_CLIPPING_PLANE 100.0
#define NUMBER_OF_MARCH_STEPS 40
#define EPSILON 0.01
#define DISTANCE_BIAS 0.7

float fmod(float a, float b)
{
    if(a<0.0)
    {
        return b - mod(abs(a), b);
    }
    return mod(a, b);
}

float udBox( vec3 p, vec3 c, vec3 b )
{
  return length(max(abs(p-c)-b,0.0));
}

// distance to sphere function (p is world position of the ray, s is sphere radius)
// from http://iquilezles.org/www/articles/distfunctions/distfunctions.htm
float sdSphere(vec3 p, vec3 c, float s)
{
    return length(p - c) - s;
}

vec2 scene(vec3 position)
{
    /*
    This function generates a distance to the given position
    The distance is the closest point in the world to that position
    */
    // to move the sphere one unit forward, we must subtract that translation from the world position
    vec3 translate = vec3(0.0, -0.5, 1.0);
    float materialID = 1.0;
    vec3 p = position - translate;
    float distance = 0.0;

    %s

    // we return a vec2 packing the distance and material of the closes object together
    return vec2(distance, materialID);
}

vec2 raymarch(vec3 position, vec3 direction)
{
    /*
    This function iteratively analyses the scene to approximate the closest ray-hit
    */
    // We track how far we have moved so we can reconstruct the end-point later
    float total_distance = NEAR_CLIPPING_PLANE;
    for(int i = 0 ; i < NUMBER_OF_MARCH_STEPS ; ++i)
    {
        vec2 result = scene(position + direction * total_distance);
        // If our ray is very close to a surface we assume we hit it
        // and return it's material
        if(result.x < EPSILON)
        {
            return vec2(total_distance, result.y);
        }

        // Accumulate distance traveled
        // The result.x contains closest distance to the world
        // so we can be sure that if we move it that far we will not accidentally
        // end up inside an object. Due to imprecision we do increase the distance
        // by slightly less... it avoids normal errors especially.
        total_distance += result.x * DISTANCE_BIAS;

        // Stop if we are headed for infinity
        if(total_distance > FAR_CLIPPING_PLANE)
            break;
    }
    // By default we return no material and the furthest possible distance
    // We only reach this point if we didn't get close to a surface during the loop above
    return vec2(FAR_CLIPPING_PLANE, 0.0);
}

void main (void) {
    vec2 uv = gl_FragCoord.xy/u_resolution.xy;

    // Our rays should shoot left and right, so we move the 0-1 space and make it -1 to 1
    uv = uv * 2.0 - 1.0;

    // // Last we deal with an aspect ratio in the window, to make sure our results are square
    // // we must correct the X coordinate by the stretching of the resolution
    // uv.x *= iResolution.x / iResolution.y;

    // Now to conver the UV to a ray we need a camera origin, like 0,0,0; and a direction
    // We can use the -1 to 1 UVs as ray X and Y, then we make sure the direction is length 1.0
    // by adding a Z component. Code blow is just an example:
    //float sqr_length = dot(uv, uv);
    //vec3 direction = vec3(uv, sqrt(1.0 - sqr_length));

    // a shorter and easier way is to create a vec3 and normalise it,
    // we can manually change the Z component to change the final FOV;
    // smaller Z is bigger FOV
    vec3 direction = normalize(vec3(uv, 2.5));
    // if you rotate the direction with a rotation matrix you can turn the camera too!

    vec3 camera_origin = vec3(0.0, 0.0, -2.5); // you can move the camera here

    vec2 result = raymarch(camera_origin, direction); // this raymarches the scene

    // now let's pick a color
    vec3 materialColor = vec3(0.0, 0.0, 0.0);
    if(result.y == 1.0)
    {
        materialColor = vec3(1.0, 0.25, 0.1);
    }
    if(result.y == 2.0)
    {
        materialColor = vec3(0.7, 0.7, 0.7);
    }

    gl_FragColor = vec4(materialColor, 1);
}

    """ % (str(shader))

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
