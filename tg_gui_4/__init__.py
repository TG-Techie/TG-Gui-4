import gc

class color():
    """
    desc: a pallette of standard colors for use in writing programs.
    standard colors includes:
    - background:   the default color used behind objects.
    - widget_background:   the default color used as a background within widgets.
    - fill:         the default body color of widgets meant to be distinct form eachother.
    - pointed_fill: the default fill when an object is being touched/hovered.
    - text:         the default color of text, should ocntract with background.
    - pointed_text: the default fill when an object is being touched/hovered.
    -
    - border:           the default border color for systems that require borders (usually monochrome).
    - pointed_border:   the default border color when an object is being touched/hovered.
    - textfield_text:       the default color of text in an interactable textfield.
    - textfield_border:     the default color of the border around a textfield.
    - textfield_background: the default color behind the text in a textfield.
    -
    - red:    24bit hex red.
    - orange: 24bit hex orange.
    - yellow: 24bit hex yellow.
    - green:  24bit hex green.
    - blue:   24bit hex blue.
    - purple: 24bit hex purple.
    -
    - black:      24bit hex black.
    - darkgray:   24bit hex darkgray.
    - gray:       24bit hex gray.
    - lightgray:  24bit hex lightgray.
    - white:      24bit hex white.
    ;
    """

    #FIXME: revisit color pallette! https://refactoringui.com/previews/building-your-color-palette/
    background              = 0x000000
    widget_background       = 0x707070
    fill                    = 0x20639b#0x20639b #0x05556e #0x173f5f
    pointed_fill            = 0x7fffff
    text                    = 0xffffff # 0xc0c0c0
    pointed_text            = 0x000000
    border                  = 0x7fffff
    pointed_border          = 0x05556e
    textfield_text          = 0x000000
    textfield_border        = 0x7f7f7f
    textfield_background    = 0xe0e0e0
    alerting                = 0xed553d
    warning                 = 0xf6d55c

    red     = 0xff0000
    orange  = 0xffa734
    yellow  = 0xffff00
    green   = 0x00ff7f #jonah like 32cd32    # 80ff30
    blue    = 0x0000ff
    purple  = 0xba55d3 #bad:   9020e0

    pink    = 0xe75480

    black       = 0x000000
    darkgray    = 0x3f3f3f
    gray        = 0x7f7f7f
    lightgray   = 0xbebebe
    white       = 0xffffff

class unit():
    """
    desc: a group of sizes for use in writing programs,
        each is a system suggested size for objects.
    sizes included:
    - small: a good size for interactable widgetson the smaller side. often combined with `unit.base` .
    - base: a good general size for interactable widgets.
    - large: a good size for interactable widgets on the larger size.
    - margin: the system default margin between objects.
    - radius: the system default for radii.
    -
    - font_size: the system standard font size, multiply.
    - char_width: the width of a charater, used for internal widget calcualtion.
    - char_height: the height of a charater, used for internal widget calcualtion.
    ;
    """
    small   = 0.6
    base    = 1.0
    large   = 1.2
    margin  = .05
    border = 0.025
    radius  = 0.2

    font_size = 0
    char_width = 1
    char_height = 1

# a backup name used when color reserved for a local variable
color_ = color

# possible action funciton names and the associated lists for
#   accumlating the widgets with that action
action_types = {
            'tap' : [],
            'alttap'    : [],
            'vslide'    : [],
            'hslide'    : [],
            #'enterchar' : [],
            'refresh'   : [],
            #'nextview'  : [],
            #'priorview' : [],
            #'aboveview' : [],
            #'belowview' : [],
            'procede' : [],
            'concede' : [],
            }

class _UniqueConstant():

    def __init__(self, name):
        self._name = name

    def __eq__(self, other):
        return self is other

    def __str__(self):
        return f"<{self._name}>"

Horizontal = _UniqueConstant('Horizontal')
Vertical = _UniqueConstant('Vertical')
X = _UniqueConstant('X')
Y = _UniqueConstant('Y')
Z = _UniqueConstant('X')

Above = _UniqueConstant('Above')
Below = _UniqueConstant('Below')
Prior = _UniqueConstant('Prior')
Next = _UniqueConstant('Next')

del _UniqueConstant

def bound_function(inst, func):
    """
    desc: bind a function to an instance of a object to simulate a bound method;
    arg <object> inst: the object to be bound to;
    args <FunctionType> func: the function to be bound;
    returns FunctionType;
    """
    return lambda *args, **kwargs: func(inst, *args, **kwargs)

def do_nothing(*args, **kwargs):
    """
    desc: two guesses;
    arg* args;
    kwarg** kwargs;
    """
    return

def widgetclass(cls):
    """
    purpose: decorator;
    desc: used ot initialize a class as a widget class;
    """
    if not (isinstance(cls, type) and issubclass(cls, widget)):
        raise ValueError("can only decorate subclasses of 'widget'")

    cls._format_subclass()
    return cls

def init(   *,
            unit_base,
            font_size,
            # optional sizing parameters
            unit_small=None,
            unit_large=None,
            unit_margin=None,
            unit_radius=None,
            # port specific tie-ins
            port_init=do_nothing,
            port_place=do_nothing,
            port_pickup=do_nothing,
            # color customization
            color_background=None,
            color_widget_background=None,
            color_fill=None,
            color_pointed_fill=None,
            color_text=None,
            color_pointed_text=None,
            color_border=None,
            color_pointed_border=None,
            color_textfield_text=None,
            color_textfield_border=None,
            color_textfield_background=None
        ):
    unit.base = unit_base

    unit.font_size = font_size

    widget._port_init = port_init
    widget._port_place = port_place
    widget._port_pickup = port_pickup

    if unit_small is None:
        unit.small = int(unit.small * unit_base)
    else:
        unit.small = unit_small

    if unit_large is None:
        unit.large = int(unit.large * unit_base)
    else:
        unit.large = unit_large

    if unit_margin is None:
        unit.margin = int(unit.margin * unit_base)
    else:
        unit.margin = unit_margin

    if unit_radius is None:
        unit.radius = int(unit.radius * unit_base)
    else:
        unit.radius = unit_radius

    if color_background is not None:
        color.background = color_background
    if color_background is not None:
        color.widget_background = color_widget_background
    if color_background is not None:
        color.fill = color_fill
    if color_background is not None:
        color.pointed_fill = color_pointed_fill
    if color_background is not None:
        color.text = color_text
    if color_background is not None:
        color.pointed_text = color_pointed_text
    if color_background is not None:
        color.border = color_border
    if color_background is not None:
        color.pointed_border = color_pointed_border
    if color_background is not None:
        color.textfield_text = color_textfield_text
    if color_background is not None:
        color.textfield_border = color_textfield_border
    if color_background is not None:
        color.textfield_background = color_textfield_background

class widget_prototype():

    def __init__(self, widcls, **kwargs):
        """
        desc: a prototype of a widget, used to specify any optional parameters
            without knowing the position or dimensions;
        arg <type> widcls: the type of the widget_prototype, must be a subclass of widget;
        kwarg** kwargs: any parameters for a final verison of the widget;
        """
        self.widcls = widcls
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """
        desc: contructs and returns a finalized version of the prototype;
        arg* args: the positional arguments used to constuct finalized version;
        returns widget: the type returned depends on the
            type specified when the prototype was made;
        """

        if len(args):
            for key, value in self.kwargs.items():
                kwargs[key] = value
            return self.widcls(*args, **kwargs)
        else:
            subkwargs = dict(self.kwargs)
            for key, value in kwargs:
                subkwargs[key] = value
            return widget_prototype(self.widcls, subkwargs)

    def __getattr__(self, attrname):
        """
        desc: default any attributes to the type of the prototype;
        """
        return getatr(self.widcls, attrname)

    def __str__(self):
        widcls = self.widcls
        if isinstance(widcls, type):
            return "<prototype {}>".format(widcls.__name__)
        else:
            return "<prototype {}>".format(str(widcls))


def onscreen_attribute(func):
    """
    purpose: decorator;
    desc: constructs a descriptor to manage attributes used when placing the
        widget or attributes that change the appearance of the widget on the
        screen. Treat the decorated funciton like a setter, name the private
        variable '_<function name>', the name of decorate function prefixed
        with an underscore. Do not decorate attributes that change the
        dimensions or boundaries of widgets, this includes radii of widgets;
    arg <func>: the function to decorate;
    """

    _name = '_'+func.__name__

    #FIXME: make sperate class for this do conserve
    #   memory space due to closures and locals
    def onscreen_attribute_appearance_wrapper(self, value):
        if value != getattr(self, _name):
            func(self, value)
            if self._on_screen:
                self.place()

    return property(lambda self: getattr(self, _name))\
            .setter(onscreen_attribute_appearance_wrapper)


def changes_appearance(func):
    #FIXME: make sperate class for this do conserve
    #   memory space due to closures and locals
    def appearance_changing_wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        if self._on_screen:
            self.place()
    return appearance_changing_wrapper

def changes_boundaries(func):
    """
    purpose: decorator;
    desc: constructs a descriptor to manage attributes used when placing the
        widget or attributes that change the appearance of the widget on the
        screen. Treat the decorated funciton like a setter, name the private
        variable '_<function name>', the name of decorate function prefixed
        with an underscore. ONLY decorate attributes that change the
        dimensions or boundaries of widgets, this includes radii of widgets;
    arg func: the function to decorate;
    """

    _name = '_'+func.__name__

    def appearance_changing_wrapper(self, value):
        if value != getattr(self, _name):
            if self._on_screen:
                self.pickup(True)
                func(self, value)
                self.place()
            else:
                func(self, value)

    return property(lambda self: getattr(self, _name))\
            .setter(appearance_changing_wrapper)


def subview(cls):
    global viewport

    if not (cls == container or cls == viewport):
        cls._subview_index = viewport._next_subview_index
        viewport._next_subview_index += 1
    elif cls._subview_index < 0:
        raise AttributeError("type '{}' cannot be used as a subview, invalid type".format(cls.__name__))
    else:
        raise AttributeError("type '{}' already designated as a subview, cannot be re-indexed".format(cls.__name__))

    return cls

class types:
    FunctionType = type(do_nothing)


#@contextmanager
class change_appearance():

    def __init__(self, wid, debug=False):
        """
        purpose: context_manager;
        desc: mange the chagning/placing of onscreen
            attributes for an instance of a widget;
        arg <widget> wid: the widget to manage;
        """
        self._wid = wid
        self._was_on_screen = None
        self.debug = debug

    def __enter__(self):
        """
        doc-type: internal;
        """
        wid = self._wid
        self._was_on_screen = is_on_screen = wid._on_screen

        if self.debug:
            print('entering appearance change:', self, is_on_screen)

        if is_on_screen:
            wid.pickup(True)
            gc.collect()

    def __exit__(self, *args):
        """
        doc-type: internal;
        """
        if self.debug:
            print('exiting appearance change:', self)
        if self._was_on_screen:
            self._wid.place()

class position_specifier():

    def __init__(self, ref):
        """
        doc-type: internal;
        desc: an intermediate representation of a coordinate used to specify the
            position of some widget(s);
        arg <widget> ref: the widget to be used as the reference point for the
            coordinate;
        """
        self._ref = ref

    def value(self, wid, dimension=None):
        """
        desc: calculate the specific position;
        """
        return None

class leftof(position_specifier):

    def value(self, wid, dimension=None):
        return self._ref.x - wid.width

class rightof(position_specifier):

    def value(self, wid, dimension=None):
        return self._ref.x +self._ref.width

class above(position_specifier):

    def value(self, wid, dimension=None):
        return self._ref.y - wid.height

class below(position_specifier):

    def value(self, wid, dimension=None):
        #print(self, self._ref)
        #print(self._ref.y, self._ref.height)
        return self._ref.y + self._ref.height

class centeredin(position_specifier):

    def value(self, wid, dimension='x'):
        if dimension == 'x':
            return self._ref.x +self._ref.width//2 - wid.width//2
        elif dimension == 'y':
            return self._ref.y +self._ref.height//2 - wid.height//2

class dimension_specifier():

    def __init__(self, ref):
        self._ref = ref

    def value(self, wid, dimension=None):
        return None

class State():

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class widget():

    _next_widget_id = 0

    _port_init = do_nothing
    _port_place = do_nothing
    _port_pickup = do_nothing

    refresh = do_nothing

    # defualt value for navigation flags
    priorview_active = False
    nextview_active  = False
    aboveview_active = False
    belowview_active = False

    @classmethod
    def _format_subclass(cls):
        """
        purpose: classmethod;
        desc: a classmethod used to format subclasses of
            a given widget subclass;
        """
        pass

    def __init__(self, x, y, width, height, *, margin=None, superior=None, **actions):
        """
        desc: the base class for all widgets;
        arg <int> x: the horizontal position of the widget;
        arg <int> y: the vertical position of the widget;
        arg <int> width: the horizontal dimension of the widget;
        arg <int> height: the horizontal dimension of the widget;
        kwarg <int> margin: the margin around the widget,
            its inset relative to its boundaries (x, y, width, height);
        kwarg** actions: a catch all for widget specific actions,
            only specify functions compliant with the associated actions;
        """

        global widget
        self._id = widget._next_widget_id
        widget._next_widget_id += 1
        #FIXME: add asserts for type checking

        if margin is None:
            margin = unit.margin
        for action in action_types:
            if (action in actions):
                setattr(self, action, bound_function(self, actions.pop(action)))

        if len(actions):
            raise ValueError("extranious keyword argument, invalid action(s) specified: {}".format(str(list(actions.keys()))[1:-1]))

        #if isinstance(superior, widget):

        #else:
        self._superior = superior

        '''if isinstance(width, dimension_specifier):
            width = width.value(self, dimension='x')

        if isinstance(height, dimension_specifier):
            height = height.value(self, dimension='y')'''

        self._width = width
        self._height = height
        self._margin = margin

        #self._x = x
        #self._y = y
        if isinstance(x, position_specifier):
            x = x.value(self, dimension='x')


        if isinstance(y, position_specifier):
            y = y.value(self, dimension='y')

        if x < 0:
            x = superior.width + x - width + 1

        if y < 0:
            y = superior.height + y - height + 1

        self._x = x
        self._y = y

        #self._cache_phys_x = None
        #self._cache_phys_y = None

        self.__phys_width = self._width - 2*margin
        self.__phys_height = self._height - 2*margin

        self._on_screen = False
        self._pointed = False

        if not hasattr(self, 'name'):
            self.name = type(self).__name__

        widget._port_init(self)



        #FIXME: add -1 negative coordinate support

    def __str__(self):
        return "<{} id:{}>".format(self.__class__.__name__, self._id)

    @property
    def superior(self):
        """
        desc: the widget containing this one;
        """
        return self._superior

    @property
    def x(self):
        """
        desc: the horizontal position of the widget's bounds in pixels relative to
            the widget's superior;
        """
        return self._x

    @property
    def y(self):
        """
        desc: the vertical position of the widget's bounds in pixels relative to
            the widget's superior;
        """
        return self._y

    @property
    def width(self):
        """
        desc: the horizontal dimension of the widget's bounds in pixels;
        """
        return self._width

    @property
    def height(self):
        """
        desc: the vertical dimension of the widget's bounds in pixels;
        """
        return self._height

    @property
    def margin(self):
        """
        desc: the inset or matign around a widget inside of its boundaries;
        """
        return self._margin

    @property
    def x_end(self):
        """
        desc: the inset or matign around a widget inside of its boundaries;
        """
        return self._x + self._width

    @property
    def y_end(self):
        """
        desc: the inset or matign around a widget inside of its boundaries;
        """
        return self._y + self._height

    @property
    def _phys_x(self):
        """
        desc: the physical x position of the widget in refence to the origin
            of the screen accounding for margin;
        """
        #return self._cache_phys_x
        if self._superior is not None:
            return self.x + self._superior._phys_x + self._margin
        else:
            return self.x  + self._margin

    @property
    def _phys_y(self):
        """
        desc: the physical x position of the widget in refence to the origin
            of the screen accounding for margin;
        """
        #return self._cache_phys_y
        if self._superior is not None:
            return self.y + self._superior._phys_y + self._margin
        else:
            return self.y  + self._margin

    @property
    def _phys_width(self):
        """
        desc: the physical width in pixels of the widget accounting for margin;
        """
        return self.__phys_width

    @property
    def _phys_height(self):
        """
        desc: the physical height in pixels of the widget accounting for margin;
        """
        return self.__phys_height

    def _phys_coordinate_in(self, x, y):
        margin = self._margin
        phys_x = self._phys_x - margin
        phys_y = self._phys_y - margin
        margin2 = margin*2
        return (phys_x <= x <= self._phys_width + phys_x + margin2) and (phys_y <= y <= self._phys_height + phys_y + margin2)

    def place(self):
        """
        desc: places a widget onto the screen;
        """

        for action, action_list in action_types.items():
            #print(self, action, hasattr(self, action))
            if hasattr(self, action) and (not self in action_list):
                action_list.append(self)

        #if hasattr(self, 'refresh'):
        self.refresh()

        self._on_screen = True

        widget._port_place(self)

    def pickup(self, visual, debug=False):
        """
        desc: removes a widget from the screen;
        """
        #print(self.pickup, visual, debug)
        if debug:
            print('widget.pickup', self, visual)

        if visual:
            widget._port_pickup(self, visual, debug=debug)

        self._on_screen = False
        self._pointed = False

        self._cache_phys_x = None
        self._cache_phys_y = None

        for action, action_list in action_types.items():
            while self in action_list:
                action_list.remove(self)

    '''
    def readout(self, *args, **kwargs):
        supr = self._superior
        return f"""{self}| superior:{supr}
                    \t    domain:\t{(self.x,self.y)}\t{(self.width,self.height)}
                    \tphyscoords:\t{(self._phys_x,self._phys_y)}\t{(self._phys_width,self._phys_height)}"""
    '''

    def _layout(self, indent=0):
        return ('\t'*indent) + str(self) + '\n'

    def pointdown(self):
        """
        desc: selects | higlights a widget;
        """
        self._pointed = True

    def pointup(self):
        """
        desc: deselects | un-higlights a widget;
        """
        self._pointed = False

class container(widget):

    _subview_index = -2

    @classmethod
    def _nested_subclass_wrap(cls, nestcls):
        """
        doc-type: internal;
        """
        def _widcls_container_wrapper(superior, *widargs, **widkwargs):
            #print(superior, widargs, widkwargs)
            if len(widargs) == 0:
                #raise Exception("widget prototyping not implemented")
                return widget_prototype(nestcls, **widkwargs)
            elif len(widargs) == 4:
                if superior not in widkwargs:
                    widkwargs['superior'] = superior
                else:
                    superior = widkwargs['superior']
                widinst = nestcls(*widargs, **widkwargs)
                superior.add(widinst)
                return widinst
            else:
                raise ValueError("invalid number of positional argument for nesting widget")
        return _widcls_container_wrapper

    @classmethod
    def _format_subclass(cls):
        # wrap all of the classws within a container class
        #   with a instantiate and nest function
        for attrname in list(dir(cls)):
            attr = getattr(cls, attrname)
            if isinstance(attr, type) and issubclass(attr, widget)\
                    and (not attrname.startswith('_'))\
                    and (not attrname.endswith('_type')):
                attr._format_subclass()
                setattr(cls, "_{}_type".format(attrname), attr)
                setattr(cls, attrname, cls._nested_subclass_wrap(attr))



    @classmethod
    def widgetclass(cls, nestcls):
        """
        desc: a decorator used to register a class as a possible subordinate
            of a the type of widget widgetclass is from.
            EX: 'container.widgetclass' means that the decotared class if now a
            widgetclass that can be used inside any container but decorating with
            'my_special_container.widgetclass' will the decorated class a
            widgetcalss of only 'my_special_container' and
            subclasses of 'my_special_container';
        arg <type> nestcls: the class being registered and turned in a widgetclass;
        """
        if not hasattr(cls, nestcls.__name__):
            setattr(cls, "_{}_type".format(nestcls.__name__), nestcls)
            setattr(cls, nestcls.__name__, cls._nested_subclass_wrap(nestcls))
        #else:
            #raise ValueError("{}")

        return widgetclass(nestcls)

    def __init__(self, *args, _build_now=True, **actions):
        """
        desc: a widget used to 'contain' other widgets relative to its own position.
            a widget(widget-a) is said to be contained by a cntr (the "TG-Gui abreviation" of container)
            if that widget can only visible on the screen if some cntr is visible.
            said container is know as the superior to that widget and teh widget
            is know as a subordinate of the cntr. a widget contained by a cntr is
            know as being 'nested' in that cntr. any given widget can only be
            contained by up to one cntr but a cntr can contain any number of widgets
            (unless otherwise limited by some feature specific to the subclass of container).
            a widget can be added to a by two means. The first is to exlicitly make an
            un-nested widget and pass it to the '.add()' method of some cntr.
            The second is to create and nest a widget to a container at the same time;
        """
        if 'margin' in actions:
            raise ValueError("'margin' not settable for 'container'")

        super().__init__(*args, margin=0, **actions)

        self._subordinates = []

        if _build_now:
            self.build()

    def build(self):
        pass

    def rebuild(self):
        #print(self, self._subordinates)
        with change_appearance(self):
            for sub in tuple(self._subordinates):
                self.remove(sub)
            gc.collect()
            #print(self._subordinates)
            self.build()
        #print(self._subordinates)


    def add(self, sub):
        #print(sub, sub._superior)
        if sub._superior is None or sub._superior is self:
            if sub not in self._subordinates:
                self._subordinates.append(sub)
            sub._superior = self

            if self._on_screen:
                sub.place()
        else:
            raise ValueError(f"{sub} nested in {sub._superior}, widget cannot be double nested")

    def remove(self, sub):
        if sub in self._subordinates:
            self._subordinates.remove(sub)
            #sub._superior = None

            if self._on_screen:
                sub.pickup(True)
        else:
            raise ValueError("{} not nested in {}, cannot remove unnested widget".format(sub, self))

    def place(self):
        super().place()
        for wid in self._subordinates:
            wid.place()

    def pickup(self, visual):
        for wid in self._subordinates:
            wid.pickup(False)
        super().pickup(visual)

    def _layout(self, indent=0):
        string = super()._layout(indent=indent)
        if not len(self._subordinates ):
            string += '\t'*(indent+1) + 'No subordinates\n'
        for wid in self._subordinates:
            string += wid._layout(indent=indent+1)
        return string

container.widgetclass(widget)
container.widgetclass(container)

@container.widgetclass
class viewport(widget):

    #enable_navigation = False

    #normal class vars
    _next_subview_index = 0

    #per class criteria
    _subviewclasses = ()
    _subview_index = -1

    #cls.state = State(
    #    subview_index = 0
    #)


    @classmethod
    def _nested_subclass_wrap(cls, nestcls):
        """
        doc-type: internal;
        """
        def _widcls_subview_wrapper(*widargs, **widkwargs):
            inst = nestcls(*widargs, **widkwargs)
            #setattr()
            return nestcls
        return _widcls_subview_wrapper

    @classmethod
    def _format_subclass(cls, debug=False):
        """
        doc-type: internal;
        """
        cls._subviewclasses = subviewclasses = []
        for attrname in dir(cls):
            attr = getattr(cls, attrname)
            if isinstance(attr, type) and issubclass(attr, widget):
                attr._format_subclass()
                subviewclasses.append(attr)
        if debug:
            print('subview classes for viewport', cls)
            print(subviewclasses, [c._subview_index for c in subviewclasses if hasattr(c, '_subview_index')])
        subviewclasses.sort(key=lambda item: item._subview_index)
        cls.state = State(
            subview_index = 0
        )

        if debug:
            print(subviewclasses, [c._subview_index for c in subviewclasses if hasattr(c, '_subview_index')])

    def __init__(self, *args, carousel=False, navigation=None, state=None, **actions):
        """
        desc: a widget used to dispay subviews of containers or other viewports.
            nest the possible subview classes inside the subview subclass;
        arg* args: the standard positonal argumets for widgets;
        kwarg <bool> carousel False: causes navigation to loop instead of
            halting navigation at when on the first or last subview;
        kwarg** actions: any actions the class subview should have;
        """

        if 'margin' in actions:
            raise ValueError("'margin' not settable for 'subview'")

        self.carousel = carousel

        self._navigation = navigation

        self._appearance_changer = change_appearance(self)


        if state is None:
            # if the class of self does not have a state object
            #   make one for this isinstance
            if not hasattr(self, 'state'):
                self.state = State(
                    subview_index=0
                )
        else:
            self.state = state

        super().__init__(*args, margin=0, **actions)

        self._subviews = subviews = [\
            sbvwcls(0, 0, self.width, self.height, superior=self)\
            for sbvwcls in self.__class__._subviewclasses
            ]

        if len(subviews):
            if not hasattr(self.state, 'subview_index'):
                self.state.subview_index = 0
        else:
            self.state.subview_index = None

    def __len__(self):
        return len(self._subviews)

    def __getitem__(self, index):
        #if view_index is not None:
        return self._subviews[index]
        #else:
        #    return None

    def __contains__(self, target):
        if isinstance(target, type) and (target in self._subviewclasses):
            return True
        elif isinstance(target, (container, viewport)) and (target in self._subviews):
            return True
        else:
            return False

    @property
    def subview(self):
        view_index = self.state.subview_index
        if view_index is not None:
            return self._subviews[view_index]
        else:
            return None

    @property
    def navigation(self):
        return self._navigation

    def append(self, mkr):
        if isinstance(mkr, widget_prototype):
            clstype = mkr.widcls
        else:
            clstype = mkr
        #print(mkr)
        #if (callable(mkr) and mkr.__name__.endswith('_wrapper'))\ or
        #if not issubclass(clstype, (container, viewport)):
        self._subviews.append(mkr(0, 0, self.width, self.height, superior=self))
        #else:
        #    raise TypeError("subviews must be subclasses of type 'container' or 'viewport'")

        # if first subview adjust index
        if len(self._subviews) == 1:
            self.state.subview_index = 0

        return self._subviews[-1]

    def switchview(self, target, _bypass=False, debug=False, _force_renav=False):

        subviews = self._subviews
        subviews_len = len(subviews)
        if debug:
            print('viewport.switchview: target=', target, 'subviews =', subviews)
        if isinstance(target, int) and (_bypass or (-subviews_len <= target < subviews_len)):
            index = target
        elif isinstance(target, type) or isinstance(target, (container, viewport)):
            index = self.index(target)
        else:
            raise ValueError("invalid input, 'target' must be: "\
                        +f" of type 'int' -{subviews_len+1} < target < {subviews_len},"\
                        + " a subview added as a 'widget_prototype',"\
                        + " or a nested subview of a viewport subclass."\
                        +f" however, got value '{target}' of type '{type(target)}'"
                        )
        if debug:
            print('index is', index)
        if self.state.subview_index != index or _force_renav:
            with self._appearance_changer:
                self.state.subview_index = index


    def index(self, target, debug=False):
        if debug:
            print('viewport.index', target)
        #print(self, target, self._subviewclasses, target in self._subviewclasses)
        if isinstance(target, type) and (target in self._subviewclasses):
            return self._subviewclasses.index(target)
        elif isinstance(target, (container, viewport))\
                and (target in self._subviews):
            return self._subviews.index(target)
        else:
            raise ValueError("object not in sequence a viewswitch 'target' must be "\
                                +"a subview added as a 'widget_prototype', got an argument "\
                                +f"of type '{type(target).__name__}' and value '{target}'"
                                )

    def remove(self, target):
        if isinstance(target, (container, viewport))\
                and (target in self._subviews)\
                and (type(target) not in self._subviewclasses):
            with self._appearance_changer:
                self._subviews.remove(target)
                self.state.subview_index = min(self.state.subview_index, len(self._subviews)-1)
        else:
            raise ValueError("object not in sequence")

    @property
    def priorview_active(self):
        return self.navigation is Horizontal\
               and not self.carousel\
               and not self.state.subview_index == 0\
               and len(self._subviews) > 1

    @property
    def nextview_active(self):
        return self.navigation is Horizontal\
               and not self.carousel\
               and not self.state.subview_index == len(self._subviews)-1\
               and len(self._subviews) > 1

    @property
    def aboveview_active(self):
        return self.navigation is Vertical\
               and not self.state.subview_index == 0\
               and len(self._subviews) > 1

    @property
    def belowview_active(self):
        return self.navigation is Vertical\
               and not self.state.subview_index == len(self._subviews)-1\
               and len(self._subviews) > 1

    def place(self):
        #print(f"placeing: {self}")
        super().place()
        if self.subview is not None:
            self.subview.place()


    def pickup(self, visual, debug=False):
        """
        doc-type: internal;
        """
        subview = self.subview
        if subview is not None:
            subview.pickup(visual)
        super().pickup(False)

    def procede(self, *args, debug=False):
        if debug:
            print(f"{self} proceding")
        index = self.state.subview_index + 1

        if self.carousel:
            index %= len(self._subviews)
        else:
            index = min(index, len(self._subviews)-1)

        if index != self.state.subview_index:
            self.switchview(index)

    def concede(self, *args, debug=False):
        if debug:
            print(f"{self} conceding")
        index = self.state.subview_index - 1

        if self.carousel:
            index %= len(self._subviews, _bypass=True)
        else:
            index = max(index, 0)
        if index != self.state.subview_index:
            self.switchview(index, _bypass=True)

    def _layout(self, indent=0):
        string = super()._layout(indent=indent)
        if not len(self._subviews):
            string += ('\t'*(indent+1) + 'No Subviews\n')
        for subview in self._subviews:
            string += subview._layout(indent=indent+1)
        return string

#resoures:
proto = container(0,0,0,0)

def _proto_add(*args, **kwargs):
    raise ValueError("proto widgets cannot be defined with position or domain")
