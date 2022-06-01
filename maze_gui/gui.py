import imageio
import drawSvg as draw
import justpy as jp
import asyncio
import logging

from aiddl_core.representation.int import Int
from aiddl_core.representation.sym import Sym
from aiddl_core.representation.tuple import Tuple
from aiddl_core.representation.key_value import KeyValue
from aiddl_core.tools.logger import Logger

import maze_model as m

def draw_state(s, g, dim, images):
    size = 40
    screen_size = dim * size
    d = draw.Drawing(screen_size,
                     screen_size,
                     origin=(0, 0),
                     displayInline=False)

    for e in s:
        sv = e.get_key()
        v = e.get_value()
        # print(sv, v)
        if sv[0] == Sym("map"):
            x = sv[1][0].int_value()
            y = sv[1][1].int_value()
            r_x = x*size
            r_y = screen_size-y*size-size
            # print(x, y)
            color = '#dde3ed'
            if v == m.WALL:
                color = '#18181a'
            elif v == m.FREE:
                color = '#dde3ed'
            elif v == m.BOX:
                color = '#915d0f'
            elif v in set([m.A1, m.A2, m.A3, m.A4, m.A5, m.AGENT]):
                color = '#ed761a'
            else:
                color = '#cf1329'
            r = draw.Rectangle(r_x,
                               r_y,
                               size,
                               size,
                               fill=color)

            d.append(r)
            r.appendTitle(str(v))

    for e in s:
        sv = e.get_key()
        v = e.get_value()
        # print(sv, v)
        if sv[0] == Sym("map"):
            x = sv[1][0].int_value()
            y = sv[1][1].int_value()
            r_x = x*size
            r_y = screen_size-y*size-size
            if v in set([m.A1, m.A2, m.A3, m.A4, m.A5]):
                text_x = x*size + 2
                text_y = screen_size - y*size - size + 8
                d.append(draw.Text(str(v),
                                   30,
                                   text_x,
                                   text_y,
                                   fill='black'))
            d.append(r)
            r.appendTitle(str(v))

    for e in g:
        if e not in s:
            sv = e.get_key()
            v = e.get_value()
            # print(sv, v)
            x = v[0].int_value()
            y = v[1].int_value()
            r_x = x*size
            r_y = screen_size-y*size-size
            color = '#cf3f13'
            r = draw.Rectangle(r_x,
                               r_y,
                               size,
                               size,
                               fill=color)
            text_x = x*size + 2
            text_y = screen_size - y*size - size + 8
            d.append(r)
            d.append(draw.Text(str(sv[1]),
                               30,
                               text_x,
                               text_y,
                               fill='black'))

    d.saveSvg('example.svg')
    d.savePng('example.png')
    images.append(imageio.imread('example.png'))
    f = open("example.svg")
    s = f.read()
    f.close()
    return s
    # d.savePng('example.png')

    # Display in Jupyter notebook
    # d.rasterize()  # Display as PNG
    # d  # Display as SVG

    # # Draw a circle
    # d.append(draw.Circle(-40, -10, 30,
    #                  fill='red', stroke_width=2, stroke='black'))


class MazeGui:
    def __init__(self, region):
        self.R = region
        self.solve_click_callbacks = []
        self.send_state_callbacks = []
        self.idx = 0
        self.num_imgs_per_state = 5

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger.setLevel(logging.INFO)
        
    def add_task_request_callback(self, f):
        self.solve_click_callbacks.append(f)
        
    def add_send_state_callback(self, f):
        self.send_state_callbacks.append(f)

    def solve_click(self, msg):
        '''Send goal.'''
        self.s, self.g = self.R.get_state_and_goal()
        self.logger.info("Sending goal.")
        for f in self.solve_click_callbacks:
            f(self.g)

    def send_state_click(self, msg):
        '''Send state.'''
        self.s, self.g = self.R.get_state_and_goal()
        self.logger.info("Sending state.")
        for f in self.send_state_callbacks:
            f(self.s)

    def display_state(self, state):
        '''Called by solution service.'''
        exec_result_text = self.my_wp.last().text
        self.my_wp.remove_component(self.my_wp.last())
        self.my_wp.remove_component(self.my_wp.last())
        self.my_wp.update()

        images = []
        draw_state(state, self.g, self.R.dim, images)
        gif_name = 'exec_%d.gif' % (self.idx)
        self.idx += 1
        imageio.mimsave(gif_name, images)
        jp.Img(a=self.my_wp, src='/static/%s' % (gif_name), alt='Execution')
        
        jp.Div(text=exec_result_text, a=self.my_wp, classes='text-xl m-2 p-2')
        asyncio.run(self.my_wp.update())
            
    def display_result(self, result):
        '''Called by solution service.'''
        self.my_wp.remove_component(self.my_wp.last())
        self.my_wp.update()
        jp.Div(text="Execution result: %s" % str(result), a=self.my_wp, classes='text-xl m-2 p-2')
        asyncio.run(self.my_wp.update())


GUI = None
button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2'


def maze_click(self, msg):
    self.obj_idx = (self.obj_idx + 1) % 12
    self.text = self.char_map[self.obj_idx]
    self.set_classes(self.color_map[self.obj_idx])
    GUI.R.m[self.y][self.x] = m.term_map[self.obj_idx]


@jp.SetRoute('/')
def main_page():
    wp = jp.WebPage()

    my_table = jp.Table(a=wp, classes='')
    for i in range(GUI.R.dim):
        my_row = jp.Tr(a=my_table, classes='')
        row = []
        for j in range(GUI.R.dim):
            cell = jp.Th(a=my_row)

            d = jp.Div(text='-',
                       a=cell, classes='w-10 text-2xl text-white bg-white border-2',
                       click=maze_click)
            d.obj_idx = 0
            d.char_map = ['-', '-', 'O', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5']
            d.color_map = ['bg-white text-white', 'bg-black text-black', 'bg-white', 'bg-green-500', 'bg-red-500', 'bg-green-500', 'bg-red-500', 'bg-green-500', 'bg-red-500', 'bg-green-500', 'bg-red-500', 'bg-green-500', 'bg-red-500']
            d.x = j
            d.y = i
            row.append(d)
        GUI.R.cells.append(row)

    submit_button = jp.Input(
        value='Request Task',
        type='submit',
        a=wp,
        classes=button_classes)
    state_button = jp.Input(
        value='Send State',
        type='submit',
        a=wp,
        classes=button_classes)
    submit_button.on('click', GUI.solve_click)
    submit_button.my_wp = wp
    submit_button.idx = 1
    state_button.on('click', GUI.send_state_click)
    state_button.my_wp = wp
    state_button.idx = 1
    jp.Div(text="No state received yet.", a=wp, classes='text-xl m-2 p-2')
    jp.Div(text="No execution result received yet.", a=wp, classes='text-xl m-2 p-2')
    GUI.my_wp = wp
    return wp
