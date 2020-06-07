from telecast import *
import PIL.ImageGrab
import cv2
import numpy as np

key_codes = {'Shift': '{VK_SHIFT}',
             'Control': '{VK_CONTROL}',
             'Insert': '{VK_INSERT}',
             'Delete': '{VK_DELETE}',
             'PageUp': '{PGUP}',
             'PageDown': '{PGDN}',
             'Home': '{VK_HOME}',
             'End': '{VK_END}'}

# General customized functions
def drink_mana(assign_slot):
    send_keys(assign_slot)

def auto_attack(assign_slot):
    send_keys(assign_slot)

def pickup(assign_slot):
    send_keys('{} down'.format(assign_slot))
    send_keys('{} up'.format(assign_slot))

# Skyler's setting functions

def drink_mana():
    send_keys("{PGUP}")

def drink_hp():
    send_keys("{PGDN}")

def auto_attack():
    send_keys('{VK_CONTROL}')

def move_left():
    send_keys('{LEFT down}')
    send_keys('{LEFT up}')

def move_right():
    send_keys('{RIGHT down}')
    send_keys('{RIGHT up}')

def pickup():
    send_keys('{z down}')
    send_keys('{z up}')
    send_keys('{z down}')
    send_keys('{z up}')
    send_keys('{z down}')
    send_keys('{z up}')
    send_keys('{z down}')
    send_keys('{z up}')
    send_keys('{z down}')
    send_keys('{z up}')

def buff_0():
    send_keys('{VK_HOME down}')
    send_keys('{VK_HOME up}')
    send_keys('{VK_HOME down}')
    send_keys('{VK_HOME up}')
    send_keys('{VK_HOME down}')
    send_keys('{VK_HOME up}')

def buff_1():
    send_keys('{VK_DELETE down}')
    send_keys('{VK_DELETE up}')
    send_keys('{VK_DELETE down}')
    send_keys('{VK_DELETE up}')
    send_keys('{VK_DELETE down}')
    send_keys('{VK_DELETE up}')

def buff_2():
    send_keys('{VK_INSERT down}')
    send_keys('{VK_INSERT up}')

def buff_3():
    send_keys('{VK_END down}')
    send_keys('{VK_END up}')

def auto_hp(percent, resOption):
    '''
    choices: 1024 x 768 (0) OR 1280 x 960 (1)
    '''

    x_start = [285, 356]
    x_end = [412, 508]
    y_start = [744, 936]
    y_end = [762, 954]

    bbox = (x_start[resOption], y_start[resOption], x_end[resOption], y_end[resOption])

    im = PIL.ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

    # pick an array to analyze current hp and full hp
    # print("HP: ", im_np[10])
    # print("Auto HP. Random percent: {}. Res Option: {}".format(percent, resOption))
    # cv2.imshow("HP", im_np)
    # cv2.waitKey()

    # return unique values and count of each unique value
    unique, counts = np.unique(im_np[10], return_counts=True)

    if (counts[0] / (x_end[resOption] - x_start[resOption])) * 100 < percent:
        print("Percent HP: ", counts[0] / (x_end[resOption] - x_start[resOption]) * 100)
        drink_hp()
        # drink hp and delay for .2s
        time.sleep(0.2)
        return True

    return False

def auto_mp(percent, resOption):
    '''
    choices: 1024 x 768 (0) OR 1280 x 960 (1)
    '''

    x_start = [424, 530]
    x_end = [551, 682]
    y_start = [744, 936]
    y_end = [762, 954]

    bbox = (x_start[resOption], y_start[resOption], x_end[resOption], y_end[resOption])

    im = PIL.ImageGrab.grab(bbox=bbox)

    im_np = np.array(im)

    # pick an array to analyze current hp and full hp

    im_np = cv2.cvtColor(im_np, cv2.COLOR_BGR2GRAY)

    # print("MP: ", im_np[10])
    # print("Auto MP. Random percent: {}. Res Option: {}".format(percent, resOption))
    # cv2.imshow("MP", im_np)
    # cv2.waitKey()

    item = 0

    # 178 is empty - 1024x768
    # 134 is empty - 1280x960
    empty = [175, 130]
    for x in range(len(im_np[10])):
        if im_np[10][x] > empty[resOption]:
            item = x
            break

    if item / (x_end[resOption] - x_start[resOption]) * 100 < percent and \
            item / (x_end[resOption] - x_start[resOption]) * 100 != 0:
        print("Percent MP: ", item / (x_end[resOption] - x_start[resOption]) * 100)
        drink_mana()
        # drink mana and delay for .2s
        time.sleep(0.2)
        return True

    return False