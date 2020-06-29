from tg_gui_4 import *

def systemroot(width, height, x=0, y=0, place=True, **kwargs):
    def root_constructor(cls):
        cls = widgetclass(cls)
        inst = cls(x, y, width, height, **kwargs)
        if place:
            inst.place()
        return inst
    return root_constructor
