from tg_gui_4 import *

def init(   *,
            rect,
            text,
            centertext,
            char_width,
            char_height
        ):

    unit.char_width = char_width
    unit.char_height = char_height

    widget.roundrect = rect
    widget.text = text
    widget.centertext = centertext

@container.widgetclass
class rect(widget):

    def __init__(self, *args, radius=None, color=None, **kwargs):
        super().__init__(*args, **kwargs)

        if radius is None:
            radius = unit.radius

        if color is None:
            color = color_.fill

        self._radius = min(self.width//2, self.height//2, radius)
        self._color = color

    @onscreen_attribute
    def color(self, value):
        self._color = value

    def place(self):
        super().place()
        self.roundrect(  self._phys_x, self._phys_y,
                    self._phys_width, self._phys_height,
                    self._color, radius=self._radius
                    )

@container.widgetclass
class label(widget):

    def __init__(self, *args, text=None, radius=None,
                    color=None, text_color=None,
                    font_size=None, margin=None,
                    **kwargs):
        #if margin is None:
            #margin = 0
        super().__init__(*args, margin=margin, **kwargs)

        if text is None:
            text = "Label{}".format(self._id)
            if len(text) > (self._phys_width//unit.char_width):
                text = "LBL{}".format(self._id)

        if radius is None:
            radius = unit.radius

        if font_size is None:
            font_size = unit.font_size

        if color is None:
            color = color_.background

        if text_color is None:
            text_color = color_.text

        self._text = ''
        self.text = text
        self._color = color
        self._text_color = text_color
        self._radius = radius
        self._font_size = (0, font_size)[font_size > 0]

    @onscreen_attribute
    def color(self, value):
        self._color = value

    @onscreen_attribute
    def text_color(self, value):
        self._text_color = value

    @onscreen_attribute
    def text(self, value):
        if '\|' in value:
            count = value.count('\|')
            value = value.replace('\|', ' '*((((self._phys_width//unit.char_width) - (len(value) -2*count)))//count))
        if self._on_screen and (len(self._text) > len(value)):
            self.roundrect(  self._phys_x, self._phys_y,
                        self._phys_width, self._phys_height,
                        self._color, radius=self._radius
                        )
        self._text = value


    def place(self):
        if (not self._on_screen):
            self.roundrect(  self._phys_x, self._phys_y,
                        self._phys_width, self._phys_height,
                        self._color, radius=self._radius
                        )
        self.centertext(self._phys_x + self._phys_width//2,
                        self._phys_y + self._phys_height//2,
                        self.text[0:self._phys_width//unit.char_width],
                        color=self._text_color,
                        background=self._color,
                        size=self._font_size
                        )
        super().place()

@container.widgetclass
class button(widget):

    def __init__(self, *args, text=None, radius=None,
                    color=None, text_color=None,
                    font_size=None, identifier=None,
                    **kwargs
                    ):

        super().__init__(*args, **kwargs)

        if text is None:
            text = "Button{}".format(self._id)
            if len(text) > (self._phys_width//unit.char_width):
                text = "BTN{}".format(self._id)

        if color is None:
            color = color_.fill

        if text_color is None:
            text_color = color_.text

        if radius is None:
            radius = unit.radius

        if font_size is None:
            font_size = unit.font_size

        self._text = ''
        self.text = text
        self._radius = min(self.width//2, self.height//2, radius)
        self._color = color
        self._text_color = text_color
        self._font_size = (0, font_size)[font_size > 0]

        self.identifier = identifier

    @onscreen_attribute
    def text(self, value):
        if '\|' in value:
            count = value.count('\|')
            value = value.replace('\|', ' '*((((self._phys_width//unit.char_width) - (len(value) -2*count)))//count))
        self._text = value

    @onscreen_attribute
    def color(self, value):
        self._color = value

    @onscreen_attribute
    def text_color(self, value):
        self._text_color = value

    def place(self):
        #FIXME: use super properly
        if not self._pointed:
            color = self._color
            text_color = self._text_color
        else:
            color = color_.pointed_fill
            text_color = color_.pointed_text
        self.roundrect(  self._phys_x, self._phys_y,
                    self._phys_width, self._phys_height,
                    color, radius=self._radius
                    )
        self.centertext(self._phys_x + self._phys_width//2,
                        self._phys_y + self._phys_height//2,
                        self.text[0:self._phys_width//unit.char_width],
                        color=text_color,
                        background=color,
                        size=self._font_size
                        )
        super().place()

    def tap(self, *args):
        pass

    def pointdown(self):
        super().pointdown()
        if self._on_screen:
            self.place()

    def pointup(self):
        super().pointup()
        if self._on_screen:
            self.place()

@container.widgetclass
class toggleswitch(widget):

    def __init__(self, *args, state=False, locked=False,
            on_toggle=do_nothing, **kwargs):
        super().__init__(*args, margin=2*unit.margin, **kwargs)
        self._state = state
        self._locked = locked
        if on_toggle is not None:
            self.on_toggle = on_toggle

    @onscreen_attribute
    def state(self, value):
        self._state = bool(value)

    def toggle(self, *args, **kwargs):
        if not self._locked:
            self.state = not self._state
            self.on_toggle(self._state)

    def tap(self, *args):
        #print('tap', self, self._state)
        self.toggle()

    @property
    def locked(self):
        return self._locked

    @changes_appearance
    def lock(self):
        self._locked = True
        return self._unlock

    @changes_appearance
    def _unlock(self):
        self._locked = False

    def place(self):
        inset = self._margin
        switch_x = self._phys_x + inset
        switch_y = self._phys_y +  inset
        switch_width = self._phys_width - 2*inset
        tab_width = (switch_width - inset)//2
        tab_height = self._phys_height - 2*inset
        empty_width = switch_width - tab_width

        if self._locked:
            tab_color = color.lightgray
        else:
            if self._state:
                tab_color = color.green
            else:
                tab_color = color.fill

        if not self._on_screen:
            self.roundrect(self._phys_x, self._phys_y,
                            self._phys_width, self._phys_height,
                            color.widget_background
                            )

        if self._state:
            #tab
            self.roundrect( switch_x + empty_width, switch_y,
                            tab_width, tab_height, tab_color)
            self.roundrect( switch_x, switch_y,
                            empty_width, tab_height, color.darkgray)

        else:
            #tab
            self.roundrect( switch_x, switch_y,
                            tab_width, tab_height, tab_color)
            self.roundrect( switch_x + tab_width, switch_y,
                            empty_width, tab_height, color.darkgray)
        super().place()
