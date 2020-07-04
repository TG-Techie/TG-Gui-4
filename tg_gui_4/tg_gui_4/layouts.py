from tg_gui_4 import *

_title = None

'''
def tg_watch_register_title(tlt):
    global _title
    tlt.text = ''
    _title = tlt

def tg_watch_update_title(tltstr):
    global _title
    if _title is not None:
        with change_appearance(_title):
            _title.text = str(tltstr)
'''

@container.widgetclass
class matrix(container):

    rows=1
    cols=1

    def __init__(self, *args, rows=None, cols=None, _build_now=True, **kwargs):

        if rows is None:
            rows = self.rows
        elif not (isinstance(rows, int) and (rows > 0)):
            raise ValueError("'rows' must be a whole number of type 'int")

        if cols is None:
            cols = self.cols
        elif not (isinstance(cols, int) and (cols > 0)):
            raise ValueError("'cols' must be a whole number of type 'int")

        self._rows = rows
        self._cols = cols

        super().__init__(*args, _build_now=False, **kwargs)

        self._entries = {}
        self._dims = (self._width//cols, self._height//rows)

        positions = []
        for y in range(rows):
            for x in range(cols):
                positions.append((x, y))

        self._positions = tuple(positions)

        if _build_now:
            self.build()

    @property
    def positions(self):
        return self._positions

    @property
    def entries(self):
        return self._entries

    def __getitem__(self, pos):
        return self._entries.get(pos)

    def __setitem__(self, pos, mkr):
        positions = self._positions
        if pos not in positions:
            raise ValueError("'pos' must be of type 'tuple' between {} -> {}".format(positions[0], positions[-1]))

        x, y = pos
        dim_width, dim_height = self._dims
        wid = mkr(x*dim_width, y*dim_height, dim_width, dim_height, superior=self)
        self.entries[pos] = wid
        self.add(wid)

@container.widgetclass
class group(container):

    def __init__(self, *args,
            source=None, direction=None,
            sections=None, **kwargs
        ):

        super().__init__(*args, _build_now=False, **kwargs)

        if source is None:
            source = []

        if direction is None:
            #print((self.height / self.width), (self.height / self.width)  > 0.9)
            if (self.height / self.width)  > 0.9:
                direction = Vertical
            else:
                direction = Horizontal
            #print(direction)

        if sections is None:
            sections = len(source)

        assert isinstance(source, list), f"argument 'source' must be of type 'list', got type '{type(source).__name__}'"
        assert direction is Horizontal or direction is Vertical, f"argument 'direction' must be of one of 'Horizontal' or 'Vertical'"
        assert isinstance(sections, int), f"argument 'sections' must be of type 'int', got type '{type(sections).__name__}'"

        self._source = source
        self._direction = direction
        self._sections = sections

        self.build()

    @property
    def direction(self):
        return self._direction

    def build(self): # build from prototypes
        count = min(self._sections, len(self._source))
        if self._direction is Horizontal:
            width = self.width//self._sections
            dims = (width, self.height)
            positions = [(width*offset, 0) for offset in range(self._sections)]
        else:
            height = self.height//self._sections
            dims = (self.width, height)
            positions = [(0, height*offset) for offset in range(self._sections)]

        source = self._source
        for index in range(count):
            self.add(source[index](*positions[index], *dims))

    def __getitem__(self, index):
        return self._subordinates[index]

@container.widgetclass
class scrollview(viewport):

    sections = 0

    def __init__(self, *args, source=None, sections=None,
            navigation=Vertical, **kwargs):

        if isinstance(source, (list, tuple)):
            source = list(source)

        if source is None:
            source = []

        super().__init__(*args, navigation=navigation, **kwargs)

        if sections is None:

            sections = self.height if self.navigation is Vertical else self.width
            sections //= unit.base

        self._sections = sections

        super().append(container) # start with one blank page

        if self._navigation is Vertical:
            self._item_dims = (self.width, self.height//self._sections)
        else:
            self._item_dims = (self.width//self._sections, self.height)

        for index, prototype in enumerate(source):
            if not (isinstance(prototype, widget_prototype) or issubclass(prototype, widget)):
                raise ValueError(f"item at index {index} in source list is not a widget prototype or widgetclass")
            else:
                self.append(prototype)

    @property
    def sections(self):
        return self._sections

    @property
    def navigation(self):
        return self._navigation

    def __getitem__(self, index):
        sections = self._sections
        return self._subviews[index//sections]._subordinates[index%sections]

    def append(self, mkr):
        if len(self._subviews[-1]._subordinates) == self._sections:
            super().append(container)

        curview = self._subviews[-1]
        curview_subs = curview._subordinates

        #self._layout()
        if len(curview_subs) == 0:
            wid = mkr(0, 0, *self._item_dims)
            curview.add(wid)
        else:
            if self._navigation is Vertical:
                wid = mkr(0, below(curview_subs[-1]), *self._item_dims)
            else:
                wid = mkr(rightof(curview_subs[-1]), 0, *self._item_dims)
            curview.add(wid)
        return curview_subs[-1]

@container.widgetclass
class navigationlink(container._button_type):

    def __init__(self, *args, destination=None, **kwargs):

        if not (isinstance(destination, type)\
                and issubclass(destination, (container, viewport))
                ):
            if destination is None:
                raise ValueError("'destination' not specified for {}".format(self))
            else:
                raise ValueError("'destination' must be a subclass of type 'container' or 'viewport'")


        if hasattr(destination, 'name'):
            text = destination.name
        else:
            text = destination.__name__

        super().__init__(*args, text=text+'\|>', **kwargs)

        self._destination = destination

    @property
    def destination(self):
        return self._destination

    def tap(self, *args):
        #self.the_matrix.the_navigation_view.switchview()
        #print('navview tap', self.superior, self.superior.superior)
        #print(self.superior.superior.superior._layout())
        '''the usual layout:
        <NavView id:32> (3)
            <scrollview 'menu' id:41> (2)
                    <container id:42> (1)
                            <navigationlink 'this wiget ie self' id:46>
                            <navigationlink id:47>
            <Destination page id:33>
                    <label id:36>
                    <label id:34>
                    <label id:35>
        '''
        #old implementation:
            ##       (1)     (2)      (3)
            #self.superior.superior.superior.switchview(self._destination)

        nav_view = self.superior.superior.superior
        while not isinstance(nav_view, navigationview):
            if nav_view is None: # not nexted in NavView
                return
            else:
                nav_view = nav_view.superior
        nav_view.switchview(self._destination)


@widgetclass
class navigationview(viewport):

    def layout(self, menu):
        if self._subview_index is None:
            self._subview_index = 0

        for cls in self._subviewclasses:
            menu.append(proto.navigationlink(destination=cls))

    def __init__(self, *args, name=None, _layout_now=True, **kwargs):

        if hasattr(self, 'rows'):
            rows = self.rows
        else:
            rows = None

        super().__init__(*args, **kwargs)

        if name is None:
            if hasattr(self, 'name'):
                name = self.name
            else:
                name = self.__class__.__name__
        elif not isinstance(name, str):
            raise ValueError("'name' must be of type 'str'")

        self.enable_navigation = False
        self._menu = menu = scrollview(0, 0, self.width, self.height,
                                     sections=rows, superior=self
                                    )
        menu.name = name
        self._subviews.insert(0, menu)
        if _layout_now:
            self.layout(menu)

    def index(self, target):
        if (target in self._subviewclasses):
            return super().index(target)+1
        else:
            return super().index(target)

    @property
    def menu(self):
        return self._menu

    def _menu_category_tap(self, inst, *args):
        #print(inst.text, inst.identifier)
        self.switchview(inst.identifier)

    def back(self, *args):
        self.switchview(0)

    @property
    def priorview_active(self):
        return self.state.subview_index != 0

    def concede(self, debug=False):
        if debug:
            print(self, self._subview_index, self.superior, self.subview, self.menu)
        if self.subview != self._menu:
            self.switchview(self._menu)
        elif isinstance(self.superior, navigationview):
            self.superior.priorview()
