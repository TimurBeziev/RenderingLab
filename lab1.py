import moderngl_window as mglw
import numpy as np

vbo_coords = np.array([
    [-0.3, 0.3, 0.0],
    [0.3, 0.3, 0.0],
    [0.3, -0.3, 0.0],
    [-0.3, -0.3, 0.0]
], dtype='f4')
vbo_colors = np.array([
    [0.0, 1.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 0.3, 1.0]
], dtype='f4')

indexes = np.array([0, 2, 1, 0, 2, 3], dtype='u4')

vertex_shader = """
#version 330

in vec3 in_coord;
in vec3 in_color;
out vec4 color;

void main() {
    gl_Position = vec4(in_coord, 1.0);
    color = vec4(in_color, 1.0);
}
"""

fragment_shader = """
#version 330

in  vec4 color;
out vec4 f_color;

void main() {
    f_color = color;
}
"""

global_width = 800
global_height = 800


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (global_width, global_height)
    title = "Colored square"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # do initialization here
        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.vao = self.ctx.vertex_array(
            self.prog,
            [
                (self.ctx.buffer(vbo_coords.tobytes()), "3f", "in_coord"),
                (self.ctx.buffer(vbo_colors.tobytes()), "3f", "in_color")
            ],
            self.ctx.buffer(indexes.tobytes())
        )

    def render(self, time, frametime):
        self.ctx.clear()
        self.vao.render()

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, min(width, height), min(width, height))
        pass


def main():
    mglw.run_window_config(Window)


if __name__ == "__main__":
    main()
