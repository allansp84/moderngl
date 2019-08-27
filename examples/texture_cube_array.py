from PIL import Image

import _example
import moderngl


class Example(_example.Example):
    title = 'Color Cube'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform mat4 Mvp;

                in vec3 in_vert;
                in vec4 in_text;
                out vec4 v_text;

                void main() {
                    gl_Position = Mvp * vec4(in_vert, 1.0);
                    v_text = in_text;
                }
            ''',
            fragment_shader='''
                #version 330

                uniform samplerCubeArray Texture;

                in vec4 v_text;
                out vec4 f_color;

                void main() {
                    f_color = texture(Texture, v_text);
                }
            ''',
        )

        vertex_data = moderngl.pack([
            -3.0, -1.0, -1.0, -1.0, -1.0, -1.0, 0.0,
            -3.0, 1.0, -1.0, -1.0, 1.0, -1.0, 0.0,
            -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 0.0,
            -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 0.0,
            -3.0, -1.0, 1.0, -1.0, -1.0, 1.0, 0.0,
            -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 0.0,
            -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
            -3.0, 1.0, 1.0, -1.0, 1.0, 1.0, 0.0,

            1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0,
            1.0, 1.0, -1.0, -1.0, 1.0, -1.0, 1.0,
            3.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0,
            3.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0,
            1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0,
            3.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0,
            3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0,
        ])

        index_data = moderngl.pack([
            0, 1, 2,
            2, 3, 0,
            4, 5, 6,
            6, 7, 4,
            0, 3, 5,
            5, 4, 0,
            3, 2, 6,
            6, 5, 3,
            2, 1, 7,
            7, 6, 2,
            1, 0, 4,
            4, 7, 1,

            8, 9, 10,
            10, 11, 8,
            12, 13, 14,
            14, 15, 12,
            8, 11, 13,
            13, 12, 8,
            11, 10, 14,
            14, 13, 11,
            10, 9, 15,
            15, 14, 10,
            9, 8, 12,
            12, 15, 9,
        ], 'i4')

        self.vbo = self.ctx.buffer(vertex_data)
        self.ibo = self.ctx.buffer(index_data)
        self.vao = self.ctx.vertex_array(self.prog, [
            self.vbo.bind('in_vert', 'in_text'),
        ], self.ibo)

        images = [Image.open('examples/data/cubemap/%s.png' % c).convert('RGB') for c in 'abcdefghijkl']
        self.texture = self.ctx.texture_from(images, array=True, cubemap=True)
        self.sampler = self.ctx.sampler(self.texture)

        self.vao.scope = self.ctx.scope(self.ctx.DEPTH_TEST, samplers=[self.sampler.assign(0)])

    def render(self, time, frame_time):
        self.ctx.screen.clear((1.0, 1.0, 1.0))
        projection = (60.0, self.aspect_ratio, 0.1, 1000.0)
        self.prog['Mvp'] = moderngl.math.camera(projection, eye=(4.0, 3.0, 2.0))
        self.vao.render()


if __name__ == '__main__':
    Example.run()