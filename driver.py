# Version 1.6
# Released Date: 8/1/2020

from screen_processing import *
from tkinter import *
from basic_functions import *
import os
from random import randint
import pygetwindow as gw
import threading
import keyboard

# GLOBAL SETTINGS
windows = ['Nine Dragons', 'MapleHome', 'MapleStory']
windowName = windows[2]

window_length_x = [1024, 1280] # Resolution
window_height_y = [768, 960] # Resolution

resOption = 0 # 0 for 1024x768 | 1 for 1280x960

is_start = 0
is_gacha = 0

is_auto_attack = 0
is_auto_mp = 0
is_auto_hp = 0
is_auto_pickup = 0
is_keep_center = 0
is_check_for_cs = 0
is_check_for_GM_regular = 0
is_check_for_GM_dungeon = 0
is_sell_eqp = 0

from_mp_global = 50 # percent
to_mp_global = 60 # p ercent
from_hp_global = 70 # percent
to_hp_global = 80 # percent
hp_mp_delay = [400, 400] # milliseconds [HP, MP]
attack_delay_global = 1000 # milliseconds
buff_delay = [200, 200, 600, 100]
buff_state = [0] * len(buff_delay)

key_options = ["String"] * len(buff_delay)

user_coor_global = (0, 0) # user coordinate
keep_center_left_wall_is_reached = False # var for keep_center
keep_center_right_wall_is_reached = False # var for keep_center
keep_center_move_delay = 500 # move delay for keep_center
keep_center_radius = 40 # var for keep_center
# GLOBAL SETTINGS

# Random Vars (to make things more random and trick lie detector)

minimap_reset_times = 0
hp_percent_random = 80
mp_percent_random = 80
random_buff_delay = [0] * len(buff_delay)
for i in range(len(buff_delay)):
    random_buff_delay[i] = randint(buff_delay[i] // 4, buff_delay[i]//2)

# Random Vars

# bbox (left_x, top_y, right_x, bottom_y)

def rescale_window():
    global windowName
    hwndMain = win32gui.FindWindow(None, windowName)
    hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

    win32gui.MoveWindow(hwndMain, 0, 0, window_length_x[resOption], window_height_y[resOption], True)
    bbox = win32gui.GetWindowRect(hwndMain)

def get_user_coord():
    global user_coor_global, minimap_reset_times, is_check_for_GM_regular
    user_coor = (0, 0)
    w_minmap = 0
    try:
        # Screen Processing
        dx = MapleScreenCapturer()
        hwnd = dx.ms_get_screen_hwnd()
        rect = dx.ms_get_screen_rect(hwnd)

        static = StaticImageProcessor(dx)
        static.update_image()
        # Screen Processing

        x_minmap, y_minmap, w_minmap, h_minmap = static.get_minimap_rect()

        user_coor = static.find_player_minimap_marker(rect=[x_minmap, y_minmap, w_minmap, h_minmap])  # tuple

        # print(user_coor)
        # print("User global coor", user_coor_global)
    except Exception as e:
        # print(e)
        if is_check_for_GM_regular == 1:
            reset_minimap()
            time.sleep(0.5)
            minimap_reset_times = minimap_reset_times + 1
        # return user_coor, w_minmap
    minimap_reset_times = 0
    return user_coor, w_minmap

def display_state_info():
    os.system('cls')
    global is_auto_hp, \
        is_auto_mp, \
        is_auto_attack, \
        is_keep_center, \
        is_auto_pickup

    print(
        f'Auto HP State: {is_auto_hp}\nAuto MP State: {is_auto_mp}\nAuto Attack State: {is_auto_attack}\nAuto Pickup State: {is_auto_pickup}\nKeep Center State: {is_keep_center}\n'
    )

    print('--- Press F12 to terminate ---')
    return

def keep_center():
    global keep_center_radius, \
        keep_center_left_wall_is_reached, \
        keep_center_right_wall_is_reached, \
        keep_center_move_delay, \
        time_at_move, \
        user_coor_global

    if not keep_center_left_wall_is_reached and not keep_center_right_wall_is_reached:
        keep_center_left_wall_is_reached = True

    try:
        user_coor, w_minmap = get_user_coord()

        # print(user_coor)
        # Why do this?
        if user_coor == 0:
            reset_minimap()
            time.sleep(0.5)
            return None

        if user_coor[0] == 0:
            reset_minimap()
            time.sleep(0.5)
            return None

        # wall = []
        wall = [user_coor_global[0] - keep_center_radius,
                user_coor_global[0] + keep_center_radius]
        # print("Wall: ", wall)

        if user_coor[0] < wall[0]: # wall left
            keep_center_left_wall_is_reached = True
            keep_center_right_wall_is_reached = False

        if user_coor[0] > wall[1]: # wall right
            keep_center_right_wall_is_reached = True
            keep_center_left_wall_is_reached = False
            # print("In Right")

        # if (datetime.utcnow() - time_at_move[0]).total_seconds() > keep_center_move_delay and \
        #         not keep_center_left_wall_is_reached:
        if not keep_center_left_wall_is_reached:
            move_left_mage()
            # print("Move Left")

        # elif (datetime.utcnow() - time_at_move[0]).total_seconds() > keep_center_move_delay and \
        #         not keep_center_right_wall_is_reached:
        else:
            move_right_mage()
            # print("Move Right")
        minimap_reset_times = 0
    except Exception as e:
        os.system('cls')
        print(e)

def lie_detector():
    return False

def main():
    global hp_percent_random, \
        mp_percent_random, \
        from_mp_global, \
        to_mp_global, \
        from_hp_global, \
        to_hp_global

    global buff_delay, \
        minimap_reset_times, \
        keep_center_move_delay, \
        random_buff_delay, \
        key_options

    global is_auto_attack, \
        is_auto_mp, \
        is_auto_hp, \
        is_auto_pickup, \
        is_keep_center, \
        is_check_for_cs, \
        is_check_for_GM_regular, \
        is_check_for_GM_dungeon

    OPTIONS = list(key_codes.keys())

    # Copy over key codes from OPTIONS to key_options for global use
    for index in range(len(buff_delay)):
        key_options[index] = OPTIONS[index]

    # Buff all when start
    for index in range(len(buff_delay)):
        buff(key_codes[OPTIONS[index]])
        time.sleep(2)

    time_at_buff = [datetime.utcnow()] * len(buff_delay)
    time_at_check = datetime.utcnow()
    time_at_GM_exist_dungeon = datetime.utcnow()
    time_at_attack = datetime.utcnow()
    time_at_hp_mp = [datetime.utcnow()] * len(hp_mp_delay)
    time_at_move = datetime.utcnow()
    while True:
        if is_start != 1:
            time.sleep(2)
            continue

        if is_sell_eqp == 1:
            sell_equipment(resOption)
            continue
        dx = MapleScreenCapturer()
        hwnd = dx.ms_get_screen_hwnd()
        rect = dx.ms_get_screen_rect(hwnd)

        static = StaticImageProcessor(dx)
        static.update_image()
        # Buffs
        for index in range(len(buff_delay)):
            if (
                buff_state[index]
                and (datetime.utcnow() - time_at_buff[index]).total_seconds()
                > random_buff_delay[index]
            ):
                buff(key_codes[key_options[index]])
                buff(key_codes[key_options[index]])
                # print("Buff %d at: " % (index + 1), get_time())
                time_at_buff[index] = datetime.utcnow()
                random_buff_delay[index] = randint(int(buff_delay[index]) // 4, int(buff_delay[index])//2)

        # AutoHP
        if (
            is_auto_hp == 1
            and (datetime.utcnow() - time_at_hp_mp[0]).total_seconds()
            > hp_mp_delay[0] / 1000
            and static.get_HP_percent() < hp_percent_random
        ):
            drink_hp()
            # print(static.get_HP_percent())
            time_at_hp_mp[0] = datetime.utcnow()
            try:
                hp_percent_random = randint(from_hp_global, to_hp_global)
            except:
                hp_percent_random = 80
        # AutoMP
        if (
            is_auto_mp == 1
            and (datetime.utcnow() - time_at_hp_mp[1]).total_seconds()
            > hp_mp_delay[1] / 1000
            and static.get_MP_percent() < mp_percent_random
        ):
            drink_mana()
            time_at_hp_mp[1] = datetime.utcnow()
            # print(static.get_MP_percent())
            try:
                mp_percent_random = randint(from_mp_global, to_mp_global)
            except:
                mp_percent_random = 80
        # AutoAttack
        if is_auto_attack == 1 and (
            datetime.utcnow() - time_at_attack
        ).total_seconds() > (attack_delay_global / 1000):
            auto_attack()
            time_at_attack = datetime.utcnow()

        # AutoPickUp
        if is_auto_pickup == 1:
            pickup()

        # It does what it says
        if is_keep_center == 1 and (
            datetime.utcnow() - time_at_move
        ).total_seconds() > (keep_center_move_delay / 1000):
            keep_center()
            time_at_move = datetime.utcnow()

        # Check for Chaos Scroll drop
        if is_check_for_cs == 1 and (datetime.utcnow() - time_at_check).total_seconds() > 60:
            try:
                if static.is_exist_chaos_scroll():
                    time_at_check = datetime.utcnow()
                    send_sms("CS Scroll some where....!!", 14699695979)
            except Exception as e:
                print(e)
        if (
            is_check_for_GM_dungeon == True
            and (datetime.utcnow() - time_at_GM_exist_dungeon).total_seconds()
            > 20
        ):
            try:
                if static.is_exist_GM_dungeon():
                    # print("GM might be here.... Come check!!")
                    send_sms("GM might be here.... Come check!!", 14699695979)
                    is_auto_attack = 0
                    is_keep_center = 0

                    is_auto_pickup = 0
                    # send_text_to_maplestory("helloo")
                    time_at_GM_exist_dungeon = datetime.utcnow()
            except:
                pass

        # Check for GM by reset_minimap (if minimap cant be found within 5 times of pressing "m"
        # => send an sms message saying GM might be available)
        if minimap_reset_times >= 7:
            send_sms("GM might be here.... Come check!!", 14699695979)
            # is_auto_attack = 0
            # is_keep_center = 0
            # is_auto_pickup = 0
            # send_text_to_maplestory("hello?")
            minimap_reset_times = 0

def ui():
    global maple_story
    # Global for True/False var
    global is_start, \
        is_auto_attack, \
        is_auto_mp, \
        is_auto_hp, \
        is_auto_pickup,\
        is_keep_center, \
        is_check_for_cs, \
        is_check_for_GM_regular, \
        is_check_for_GM_dungeon, \
        is_sell_eqp, \
        resOption, \
        buff_state
    # Global for string/int var
    global to_mp_global, \
        to_hp_global, \
        from_mp_global, \
        from_hp_global, \
        attack_delay_global, \
        keep_center_radius, \
        keep_center_move_delay, \
        user_coor_global, \
        buff_delay, \
        key_options

    root = Tk()
    # UI Vars
    is_auto_hp = BooleanVar(value=bool(is_auto_hp))
    is_auto_mp = BooleanVar(value=bool(is_auto_mp))
    is_auto_attack = BooleanVar(value=bool(is_auto_attack))
    is_auto_pickup = BooleanVar(value=bool(is_auto_pickup))
    is_keep_center = BooleanVar(value=bool(is_keep_center))
    is_check_for_cs = BooleanVar(value=bool(is_check_for_cs))
    is_check_for_GM_regular = BooleanVar(value=bool(is_check_for_GM_regular))
    is_check_for_GM_dungeon = BooleanVar(value=bool(is_check_for_GM_dungeon))
    is_sell_eqp = BooleanVar(value=bool(is_sell_eqp))

    fromHpEntry = StringVar()
    fromHpEntry.set(str(from_hp_global))
    toHpEntry = StringVar()
    toHpEntry.set(str(to_hp_global))

    fromMpEntry = StringVar()
    fromMpEntry.set(str(from_mp_global))
    toMpEntry = StringVar()
    toMpEntry.set(str(to_mp_global))

    attackDelayUI = StringVar()
    attackDelayUI.set(str(attack_delay_global))

    keepCenterRadiusUI = StringVar()
    keepCenterRadiusUI.set(str(keep_center_radius))
    keepCenterMoveDelayUI = StringVar()
    keepCenterMoveDelayUI.set(str(keep_center_move_delay))

    userCoordinateUI = StringVar()
    userCoordinateUI.set('({}, {})'.format(user_coor_global[0], user_coor_global[1]))

    buff_reset_time = []
    buff_state_ui = []
    # UI Vars ---
    for index in range(len(buff_delay)):
        varTime = StringVar()
        varTime.set(str(buff_delay[index]))
        varState = IntVar()
        varState.set(0)
        buff_reset_time.append(varTime)
        buff_state_ui.append(varState)

    tkResOption = IntVar()
    tkResOption.set(0)  # 0 for 1024x768 | 1 for 1280x960

    # UI Vars
    # tab_parent = ttk.Notebook(root)
    # tab1 = ttk.Frame(tab_parent)
    # tab2 = ttk.Frame(tab_parent)
    # tab_parent.add(tab1, text='Tab 1')
    # tab_parent.add(tab2, text='Tab 2')
    # tab_parent.pack(expand=1, fill='both')
    root.title("MapleStory Helper")


    def change_auto_mp_state():
        global is_auto_mp
        is_auto_mp = toggle(is_auto_mp)
        # print("Auto MP state", is_auto_mp)
        maple_story.activate()

    def change_auto_hp_state():
        global is_auto_hp
        is_auto_hp = toggle(is_auto_hp)
        # print("Auto HP state", is_auto_hp)
        maple_story.activate()

    def change_auto_attack_state():
        global is_auto_attack
        is_auto_attack = toggle(is_auto_attack)
        maple_story.activate()

    def change_auto_pickup_state():
        global is_auto_pickup
        is_auto_pickup = toggle(is_auto_pickup)
        # print("Auto pick up state", is_auto_pickup)
        maple_story.activate()

    def change_keep_center():
        global is_keep_center
        is_keep_center = toggle(is_keep_center)
        maple_story.activate()

    def change_check_for_cs():
        global is_check_for_cs
        is_check_for_cs = toggle(is_check_for_cs)
        # print(is_check_for_cs)
        maple_story.activate()
        return

    def change_check_for_GM_regular():
        global is_check_for_GM_regular
        is_check_for_GM_regular = toggle(is_check_for_GM_regular)
        return

    def change_check_for_GM_dungeon():
        global is_check_for_GM_dungeon
        is_check_for_GM_dungeon = toggle(is_check_for_GM_dungeon)
        # print(is_check_for_GM_dungeon)
        return

    def change_sell_eqp():
        global is_sell_eqp
        is_sell_eqp = toggle(is_sell_eqp)
        # print(is_check_for_GM_dungeon)
        return

    def toggle_resolution():
        global resOption, windowName
        resOption = tkResOption.get()
        hwndMain = win32gui.FindWindow(None, windowName)
        win32gui.MoveWindow(hwndMain, 0, 0, window_length_x[resOption], window_height_y[resOption], True)
        maple_story.activate()

    def setHpRange():
        global from_hp_global, to_hp_global
        try:
            from_hp_global = int(fromHpEntry.get())
            to_hp_global = int(toHpEntry.get())
            if from_hp_global > to_hp_global:
                to_hp_global = from_hp_global + 5
            # print("HP here: ", from_hp_global , to_hp_global)
        except:
            from_hp_global = 50
            to_hp_global = 50
            print("Invalid input HP")

    def setMpRange():
        global from_mp_global, to_mp_global
        try:
            from_mp_global = int(fromMpEntry.get())
            to_mp_global = int(toMpEntry.get())
            if from_mp_global > to_mp_global:
                to_mp_global = from_mp_global + 5
            # print("MP here: ", from_mp_global , to_mp_global)
        except:
            from_mp_global = 50
            to_mp_global = 50
            print("Invalid input MP")

    def set_attack_delay():
        global attack_delay_global
        try:
            attack_delay_global = int(attackDelayUI.get())
            # print("MP here: ", from_mp_global , to_mp_global)
        except TypeError:
            attack_delay_global = 100
            print("Invalid input Attack Delay")

    def set_keep_center_radius_and_move_delay():
        global keep_center_radius, keep_center_move_delay
        try:
            keep_center_radius = int(keepCenterRadiusUI.get())
            keep_center_move_delay = int(keepCenterMoveDelayUI.get())

        except:
            keep_center_radius = 15
            keep_center_move_delay = 2000
            print("Invalid input radius or move delay")

    def get_user_coordinate_center_point_ui():
        global user_coor_global
        try:
            user_coor_global, w_random = get_user_coord()
            userCoorLabel['text'] = '({}, {})'.format(user_coor_global[0], user_coor_global[1])
        except:
            user_coor_global = (0, 0)
            userCoorLabel['text'] = '(0, 0)'

    def re_assign_time_and_key_buff(num):
        for var in range(len(var_list)):
            key_options[var] = var_list[var].get()
            buff_delay[var] = buff_reset_time[var].get()
            buff_state[var] = buff_state_ui[var].get()

    def update_status():
        return

    def toggle_start_stop():
        global is_start
        is_start = toggle(is_start)
        print("Start state: ", is_start)

    def panic():
        os._exit(0)

    # Some variables to use
    canvas_width = 100
    canvas_height = 10
    OPTIONS = list(key_codes.keys())
    # Some variables to use

    #default panel size
    root.geometry('{}x{}'.format(650, 700)) #Width x Height

    # Auto HP Row
    row = 0
    auto_hp_checkbutton = Checkbutton(root,
                                      text='Auto HP',
                                      command=change_auto_hp_state,
                                      variable=is_auto_hp,
                                      )

    auto_hp_checkbutton.grid(row=row,
                             column=0)

    auto_hp_checkbutton.var = is_auto_hp

    fromHpLabel = Label(root,
                        text="From:"
                        ).grid(column=1,
                               row=row)
    Entry(root,
          textvariable=fromHpEntry,
          width=8).grid(column=2,
                        row=row)

    toHpLabel = Label(root,
                      text="To:"
                      ).grid(column=3,
                             row=row)
    Entry(root,
          textvariable=toHpEntry,
          width=8
          ).grid(column=4,
                 row=row)

    Button(root,
           text='Set',
           command=setHpRange
           ).grid(column=5,
                  row=row)
    # line
    row += 1
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height)
    w.grid(row=row)

    y = int(canvas_height / 2)
    w.create_line(0, y, canvas_width, y, fill="#476042")
    #Auto HP Row ---

    #Auto MP Row
    row += 1
    auto_mp_checkbutton = Checkbutton(root,
                                      text='Auto MP',
                                      command=change_auto_mp_state,
                                      variable=is_auto_mp,
                                      )

    auto_mp_checkbutton.grid(column=0,
                             row=row)

    auto_mp_checkbutton.var = is_auto_mp

    fromMpLabel = Label(root,
                        text="From:"
                        ).grid(column=1,
                               row=row)
    Entry(root,
          textvariable=fromMpEntry,
          width=8
          ).grid(column=2,
                 row=row)

    toMpLabel = Label(root,
                      text="To:"
                      ).grid(column=3,
                             row=row)
    Entry(root,
          textvariable=toMpEntry,
          width=8
          ).grid(column=4,
                 row=row)

    Button(root,
           text='Set',
           command=setMpRange
           ).grid(column=5,
                  row=row)

    # line
    row += 1
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height)
    w.grid(row=row)

    y = int(canvas_height / 2)
    w.create_line(0, y, canvas_width, y, fill="#476042")
    #Auto MP Row ---

    #Auto Attack Row
    row += 1
    auto_attack_checkbutton = Checkbutton(root,
                                          text='Auto Attack',
                                          command=change_auto_attack_state,
                                          variable=is_auto_attack,
                                          )

    auto_attack_checkbutton.grid(row=row,
                                 column=0,
                                 sticky=W)

    auto_attack_checkbutton.var = is_auto_attack

    Label(root,
          text="Attack Delay (ms):"
          ).grid(column=1,
                 row=row)

    Entry(root,
          textvariable=attackDelayUI,
          width=8).grid(column=2,
                        row=row)

    Button(root,
           text='Set',
           command=set_attack_delay
           ).grid(column=5,
                  row=row)
    #Auto Attack Row ---

    #Auto Pickup Row
    row += 1
    auto_pickup_checkbutton = Checkbutton(root,
                                          text='Auto Pickup',
                                          command=change_auto_pickup_state,
                                          variable=is_auto_pickup,
                                          )

    auto_pickup_checkbutton.grid(row=row,
                                 column=0,
                                 sticky=W)

    auto_pickup_checkbutton.var = is_auto_pickup
    #Auto Pickup Row ---

    #Keep Center Row
    row += 1
    keep_center_checkbutton = Checkbutton(root,
                                          text='Keep Center',
                                          command=change_keep_center,
                                          variable=is_keep_center,
                                          )

    keep_center_checkbutton.grid(row=row,
                                 column=0,
                                 sticky=W)

    keep_center_checkbutton.var = is_keep_center

    Label(root,
          text="Radius:"
          ).grid(column=1,
                 row=row)

    Entry(root,
          textvariable=keepCenterRadiusUI,
          width=8).grid(column=2,
                        row=row)

    Label(root,
          text="Move Delay (ms):"
          ).grid(column=3,
                 row=row)

    Entry(root,
          textvariable=keepCenterMoveDelayUI,
          width=8).grid(column=4,
                        row=row)

    Button(root,
           text='Set',
           command=set_keep_center_radius_and_move_delay
           ).grid(column=5,
                  row=row)
    row += 1
    Button(root,
           text="Get User \nPosition",
           command=get_user_coordinate_center_point_ui
           ).grid(column=1,
                  row=row)
    userCoorLabel = Label(root,
                          text=userCoordinateUI
                          )

    userCoorLabel.grid(column=2,
                       row=row)

    #Keep Center Row ---

    #1024x768 resolution
    row += 1
    Radiobutton(root,
                text="1024x768",
                command=toggle_resolution,
                variable=tkResOption,
                value=0
                ).grid(row=row,
                       column=0,
                       sticky=W)

    #1280x920 resolution
    row += 1
    Radiobutton(root,
                text="1280x920",
                command=toggle_resolution,
                variable=tkResOption,
                value=1
                ).grid(row=row,
                       column=0,
                       sticky=W)

    #Buff Rows
    var_list = []
    for pos in range(4):
        row += 1
        Checkbutton(root,
                    text='Buff {}'.format(str(pos + 1)),
                    variable=buff_state_ui[pos],
                    command=lambda x=index: re_assign_time_and_key_buff(x)
                    ).grid(column=0,
                           row=row)
        Label(root,
              text="Reset Time (s):").grid(column=1,
                                       row=row)
        Entry(root,
              textvariable=buff_reset_time[pos],
              width=8
              ).grid(column=2,
                     row=row)

        Label(root,
              text="Key:"
              ).grid(column=3,
                     row=row)

        #https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
        variable = StringVar(root)
        variable.set(OPTIONS[pos])  # default value
        var_list.append(variable)
        optionMenu = OptionMenu(root, var_list[pos], *OPTIONS)
        optionMenu.grid(row=row,
                        column=4)
        #https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter

        Button(root,
               text='Set',
               command=lambda x=index: re_assign_time_and_key_buff(x)
               ).grid(column=5,
                      row=row)

        # line
        row += 1
        w = Canvas(root,
                   width=canvas_width,
                   height=canvas_height)
        w.grid(row=row)

        y = int(canvas_height / 2)
        w.create_line(0, y, canvas_width, y, fill="#476042")
    #Buff Rows ---

    #Check for Chaos Scroll Row
    row += 1
    check_cs_checkbutton = Checkbutton(root,
                                       text='Check for Chaos Scroll',
                                       command=change_check_for_cs,
                                       variable=is_check_for_cs,
                                       )

    check_cs_checkbutton.grid(row=row,
                              column=0,
                              sticky=W)

    check_cs_checkbutton.var = is_check_for_cs
    #Check for Chaos Scroll Row ---

    #Check for GM Regular Row
    row += 1
    checkGM_regular_checkbutton = Checkbutton(root,
                                              text='Check for GM Regular',
                                              command=change_check_for_GM_regular,
                                              variable=is_check_for_GM_regular,
                                              )

    checkGM_regular_checkbutton.grid(row=row,
                                     column=0,
                                     sticky=W)

    checkGM_regular_checkbutton.var = is_check_for_GM_regular
    #Check for GM Regular Row ---

    #Check for GM Dungeon Row
    row += 1
    checkGM_dungeon_checkbutton = Checkbutton(root,
                                              text='Check for GM Dungeon',
                                              command=change_check_for_GM_dungeon,
                                              variable=is_check_for_GM_dungeon,
                                              )

    checkGM_dungeon_checkbutton.grid(row=row,
                                     column=0,
                                     sticky=W)

    checkGM_dungeon_checkbutton.var = is_check_for_GM_dungeon
    #Check for GM Dungeon Row ---

    #Sell Equipment Row
    row += 1
    sell_eqp_checkbutton = Checkbutton(root,
                                       text='Sell Equipment',
                                       command=change_sell_eqp,
                                       variable=is_sell_eqp,
                                        )

    sell_eqp_checkbutton.grid(row=row,
                              column=0,
                              sticky=W)

    sell_eqp_checkbutton.var = is_sell_eqp
    #Sell Equipment Row ---

    #Notes (Text)
    row += 1
    note_text = Label(root,
                      text="Notes:"
                           "\nF3 to toggle Auto Attack."
                           "\nF4 to toggle Auto Pickup."
                           "\nF8 to toggle Keep Center."
                           # "\nF9 to toggle Move Around."
                           "\nF12 to START/STOP Helper."
                      )
    note_text.grid(row=row, sticky=W)

    #START/STOP button
    row += 1
    Button(root,
           text='START/STOP (F12)',
           command=toggle_start_stop,
           height=4,
           width=16,
           ).grid(column=5,
                  row=row)

    root.mainloop()

    return

def on_press_reaction(event):
    #https://stackoverflow.com/questions/47184374/increase-just-by-one-when-a-key-is-pressed/47184663
    global is_start, \
        is_auto_attack, \
        is_auto_pickup, \
        is_move_left, \
        is_move_right, \
        is_keep_center

    if event.name == 'f1': # info
        display_state_info()
    if event.name == 'f3': # attack
        is_auto_attack = toggle(is_auto_attack)
    if event.name == 'f4': # pick up
        is_auto_pickup = toggle(is_auto_pickup)
    if event.name == 'f8':
        is_keep_center = toggle(is_keep_center)
    if event.name == 'f12':
        is_start = toggle(is_start)

if __name__ == '__main__':
    keyboard.on_press(on_press_reaction)
    try:
        maple_story = gw.getWindowsWithTitle(windowName)[0] # Get window by name
    except:

        print("Can't find MapleStory Client... Exiting")
        exit(0)

    maple_story.activate() # Bring window on top

    rescale_window()

    print("Connected!")
    time.sleep(1)

    if is_gacha:
        while True:
            exchange_maple_coins_monstercarnival()
            time.sleep(randint(1, 4))
            mouse.click(button='left', coords=(50, 50))
    else:
        threading.Thread(target=ui).start()
        threading.Thread(target=main).start()


# import wmi
# c = wmi.WMI()
# for process in c.Win32_Process():
#   print(process.ProcessId, process.Name)