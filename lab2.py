import moderngl
import moderngl_window as mglw

from moderngl_window import geometry
from pyrr import Matrix33

vertex_shader = """
#version 330
in vec3 in_position;
in vec2 in_texcoord_0;
uniform mat3 rotation;
out vec2 uv;
void main() {
    gl_Position = vec4(rotation * in_position, 3.0);
    uv = in_texcoord_0;
}
"""

fragment_shader = """
#version 330
in vec2 uv;

uniform sampler2DArray texture0;
uniform float layers;
uniform float time;

out vec4 color;


void main() {
    float layer = floor(time);
    vec4 c1 = texture(texture0, vec3(uv, mod(layer, layers)));
    vec4 c2 = texture(texture0, vec3(uv, mod(layer + 1.0, layers)));
    float t = mod(time, 1.0);
    color = (c1 * (1.0 - t) + c2 *t) + vec4(0.1);
}
"""

global_width = 800
global_height = 800


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (global_width, global_height)
    title = "Cube"
    resource_dir = '.'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cube = geometry.cube()
        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.texture = self.load_texture_array('texture.jpg', layers=10, mipmap=True, anisotropy=100.0)
        self.prog['texture0'].value = 0
        self.prog['layers'].value = 10
        self.rotation = self.prog['rotation']

    def render(self, time: float, frametime: float):
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.rotation.value = tuple(
            Matrix33.from_eulers((time, 0.1, time * 10)).reshape(9).tolist())
        self.prog['time'].value = time
        self.texture.use(location=0)
        self.cube.render(self.prog)

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, min(width, height), min(width, height))


def main():
    mglw.run_window_config(Window)


if __name__ == "__main__":
    main()
