import sys
sys_stdout_write = print

import gc
gc_collect = gc.collect

from tg_gui_4 import action_types, do_nothing

sliding_threshold = 0
hold_time = 1
refresh_interval = 1

twas_touched = False # has the screen been physivally touched?
twas_pointed = False # has tappable been pointed
slid = False # has finger slid since last touchdown
held = False # has finger held since last touchdown

point_x, point_y = -0x1701D, -0x1701D # default values + also startek

x, y = -0x1701D, -0x1701D # default values + also startek

point_time = -0x1701D # the time the tappable was pointed
loop_time = -0x1701D # the time the current iteration of the loop started
last_refresh_time  = -0x1701D

tappable = None
slidable = None
alttappable = None
slidemethod = ''

top_edge_swipe_fn = None

enable_edge_swipes_bool = True

homebar_thresh   = 247
notif_bar_thresh = -6
left_bar_thresh  = -1
right_bar_thresh = 241


def init(   *,
            _enable_edge_swipes=False,
            top_edge_swipe=do_nothing,
            bottom_edge_swipe=do_nothing,
            left_edge_swipe=do_nothing,
            right_edge_swipe=do_nothing
            ):
    global enable_edge_swipes_bool
    enable_edge_swipes_bool = _enable_edge_swipes

    global top_edge_swipe_fn
    top_edge_swipe_fn = top_edge_swipe

    global bottom_edge_swipe_fn
    bottom_edge_swipe_fn = bottom_edge_swipe

    global left_edge_swipe_fn
    left_edge_swipe_fn = left_edge_swipe

    global right_edge_swipe_fn
    right_edge_swipe_fn = right_edge_swipe



def loop(next_xy, is_touched, next_loop_time, debug=False):
    global gc_collect
    gc_collect()

    global x, y, last_x, last_y, point_x, point_y
    global last_loop_time, loop_time, point_time, last_refresh_time
    global twas_touched, twas_pointed, slid, held
    global tappable, slidable, alttappable, slidemethod

    if (loop_time - last_refresh_time) >= refresh_interval:
        last_refresh_time = loop_time
        for wid in action_types['refresh']:
            wid.refresh()

    last_loop_time = loop_time
    loop_time = next_loop_time

    #current_touch = ft.touched
    if is_touched:
            #if debug:
            #    print('touched')

            if not twas_touched:
                last_x, last_y = next_xy
            else:
                last_x = x
                last_y = y

            x, y = next_xy


            #print(x, y)
            dx = x - last_x # delta x but physicsy
            dy = y - last_y # delta y but physicsy
            dx_mag = abs(dx) # delta x's magnitude
            dy_mag = abs(dy) # delta y's magnitude

            is_sliding = (dx_mag > 1) or (dy_mag > 1)#(dx_mag < sliding_threshold) or (dy_mag < sliding_threshold)

            if not twas_touched:# and tappable != None:
                twas_touched = True
                twas_pointed = False
                slid = False
                held = False


                point_time = loop_time
                if enable_edge_swipes_bool:
                    if (y >= homebar_thresh) and (dy <= 0): # go home

                            sys_stdout_write(('swipe up: home\n'))
                            bottom_edge_swipe_fn()
                            return
                    elif (y <= notif_bar_thresh) and (dy <= 0): # go home

                            sys_stdout_write(('swipe down: notif\n'))
                            top_edge_swipe_fn()
                            #root.switch(face)
                            return
                    elif (x >= right_bar_thresh) and (dy <= 0): # go home

                            sys_stdout_write(('swipe left\n'))
                            right_edge_swipe_fn()
                            return
                    elif (x <= left_bar_thresh) and (dy <= 0): # go home

                            sys_stdout_write(('swipe right\n'))
                            left_edge_swipe_fn()
                            return

                #find subs
                #tappable, slidable, alttappable = my_host.update_pointer(x, y, True)
                for wid in  action_types['tap']:#g_gui_3._tappables):
                    wid_x = wid._phys_x
                    wid_y = wid._phys_y
                    if (wid_x <= x <= wid.width + wid_x) and (wid_y <= y <= wid.height + wid_y):
                        tappable = wid#next_tappable_widget = wid
                        break
                else:
                    tappable = None#next_tappable_widget = pointless_pointable

                for wid in  action_types['alttap']:
                    wid_x = wid._phys_x
                    wid_y = wid._phys_y
                    if (wid_x <= x <= wid.width + wid_x) and (wid_y <= y <= wid.height + wid_y):
                        alttappable = wid#next_tappable_widget = wid
                        break
                else:
                    alttappable = None#next_slidable_widget = pointless_pointable

                point_x = x
                point_y = y
                #point_phys_x = phys_x
                #point_phys_y = phys_y



                if (tappable is not None) and twas_touched and not slid:# and (not is_sliding):
                    tappable.pointdown()
                    twas_pointed = True

            #determine the slidemethod name and asocciated list
            if is_sliding and not slid:
                # if is horizontal slide
                if dx_mag > dy_mag:
                    slide_direction = 'h'
                    current_slidables = action_types['hslide']
                else:
                    slide_direction = 'v'
                    current_slidables =  action_types['vslide']

                if not slid: # find the slidable that is targeted
                    for wid in  action_types['refresh']:
                        wid_x = wid._phys_x
                        wid_y = wid._phys_y
                        if (wid_x <= x <= wid.width + wid_x) and (wid_y <= y <= wid.height + wid_y) and hasattr(wid, slidemethod):
                            slidable = wid#next_tappable_widget = wid
                            break
                    else:
                        slidable = None #next_slidable_widget = pointless_pointable

            #if debug:
            #    print(loop_time,
            #            ('twas_touched', twas_touched),
            #            ('twas_pointed', twas_pointed),
            #            ('slid', slid),
            #            ('held', held),
            #            ('tappable', tappable),
            #            ('alttappable', alttappable),
            #            ('slidable', slidable),
            #            ('slidemethod', slidemethod),
            #        )

            if tappable is not None:
                if (not is_sliding) and (not twas_pointed):
                    #if debug:
                    #    pirnt('pointdowning tappable', tappable)
                    twas_pointed = True
                    tappable.pointdown()
                    return

            if alttappable is not None:
                if (not slid) and (not held) and ((loop_time - point_time) > hold_time):
                    #if debug:
                    #    print('alttaping:', tappable)
                    held = True
                    alttappable.alttap(x - alttappable._phys_x, y - alttappable._phys_y)
                    return

            if slidable is not None:
                if slid and twas_pointed:
                    if tappable is not None:
                        tappable.pointup()

                slid = True
                #slidefunc = getattr(slidable, slidemethod)

                if slide_direction == 'h':
                    slidable.hslide(point_y - slidable._phys_y, (point_y - y))
                    #if debug:
                    #    print('sliding h:', slidable, point_y - slidable._phys_y, (y - point_y))
                else:
                    slidable.vslide(point_x - slidable._phys_y , (point_x - x))
                    #if debug:
                    #    print('sliding v:', slidable, point_x - slidable._phys_y , (x - point_x))
                return

    elif twas_touched:
            #if debug:
            #    print('not touched')
            #    print(twas_touched, twas_pointed, held, slid, '|', tappable, alttappable, slidable, slidemethod)

            twas_touched = False

            if (tappable is not None):
                #if debug:
                #    print(tappable, 'is not None')
                if (not slid) and (not held):
                    # make sure pointer in button to tap it, if moved off don't tap
                    if tappable._phys_coordinate_in(x,y):
                        #if debug:
                        #    print('not slid and not held:', 'tapping tappable:', tappable)
                        tappable.tap(last_x - tappable._phys_x, last_y - tappable._phys_y)

                if twas_pointed and tappable in action_types['tap']:
                    #if debug:
                    #    print('pointuping tappable:', tappable)
                    tappable.pointup()

            if slid and (slidable is not None):
                slidable.endslide()

            #reset loop vars
            twas_touched = False
            twas_pointed = False
            slid = False
            held = False

            tappable, alttappable, slidable = None, None, None

            gc.collect()
