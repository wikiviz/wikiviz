from random import random
import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from controller.network.network import NetworkRequest
import model.model as mod




class NodeWidget(Widget):

    def __init__(self, **kwargs):
        radius = 15.
        # override draw method
        # with self.canvas:
        #     Ellipse(pos=self.pos, size=(radius*2, radius*2))
        #     if parent_node:
        #         Line(points=[parent_node[0], parent_node[1], self.pos[0], self.pos[1]], width=1.0)
        super(NodeWidget, self).__init__(**kwargs)


class GraphWidget(Widget):
    center_point = (Window.width/2, Window.height/2)
    all_nodes = []
    root_widget = None
    model = mod.Model()

    def add_root_node(self, keyword):
        # draw root
        print "drawing root"
        root = NodeWidget()
        root.pos = self.center_point
        self.add_widget(root)
        self.all_nodes.append(root)
        self.root_widget = root

        # get page data and update root node on completion
        nr = NetworkRequest(root, self.update_node)
        nr.get_page_by_keyword(keyword)


    def update_node(self, model_node):
        # called as callback from model update
        if model_node.parent == None:
            print "updating node widget with model ref"
            model_node.set_ui_reference(self.root_widget)
        else:
            ui_node = model_node.get_ui_reference()
            ui_node.pos = (pos[0]+40, pos[1]+40)


    def add_children(self, parent_node_widget):
        # draw children of given node
        print "drawing root"
        with self.canvas:
            degrees_each = 360/total_children
            radians_each = math.radians(degrees_each)
            parent_node_pos = center_point
            if parent_node_widget:
                parent_node_pos = parent_node_widget.pos

            for idx in range(0,total_children):
                rads = radians_each * idx
                x_pos = child_dist * math.cos(rads) + parent_node_pos [0]
                y_pos = child_dist * math.sin(rads) + parent_node_pos [1]
                print "drawing child", idx, "rads:", rads, "x:", x_pos, "y:", y_pos
                node = NodeWidget()
                node.pos = (x_pos, y_pos)
                self.add_widget(node)


    def on_touch_down(self, touch):
        pass

    def on_touch_move(self, touch):
        pass


class MyApp(App):

    def build(self):
        parent = Widget()
        graph_widget = GraphWidget()
        search_btn = Button(text='Search',
            size_hint=(.2, .2),
            pos=(20, 20))
        layout = FloatLayout(size=(Window.width, Window.height))
        layout.add_widget(graph_widget)
        layout.add_widget(search_btn)


        def search(obj):
            graph_widget.add_root_node("Mozart")

            # controller.create_children_nodes(graph_widget.root_widget, 5)
        search_btn.bind(on_release=search)


        return layout


if __name__ == '__main__':
    MyApp().run()