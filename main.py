import threading
import time
import timeit

from com.dtmilano.android.viewclient import ViewClient

import CsvCreator as csv
import helpers as h
from interactions import VirtualScrolling, OpenCloseDrawer
from perfs import Vmstat

device, serialno = ViewClient.connectToDeviceOrExit()
vc = ViewClient(device, serialno)
info = device.getDisplayInfo()
ocd = OpenCloseDrawer(device, serialno)
vs = VirtualScrolling(device, serialno)

apps = [
    {
        "type": "Android-native",
        "package": "at.marbeit.myapplication",
        "activity": "MainActivity"
    },
    {
        "type": "Android-react",
        "package": "com.perfomancetest",
        "activity": "MainActivity"
    },
    {
        "type": "Android-flutter",
        "package": "com.example.test01",
        "activity": "MainActivity"
    },
    {
        "type": "Android-ionic",
        "package": "io.ionic.starter",
        "activity": "MainActivity"
    }
]

interactions = [
    # {
    #    "name": "drawer",
    #    "runs": 3
    # }#,
    {
        "name": "switching_pages",
        "runs": 4
    }  # ,
    # {
    #    "name": "list_swipe",
    #    "runs": 4
    # }
]

coords = {
    'start_x': 0,
    'start_y': 0,
    'end_x': 0,
    'end_y': 0
}

PATH_DATA = '/Users/paulaengelberg/Desktop/i/data/'


def print_header(current_interaction, counter):
    print ('___________Interaction: {}, Round: {}___________'.format(current_interaction, counter))


def print_calculated_coords(current_interaction):
    if current_interaction == 'close_drawer':
        print(
            '{} coordinates: start_x: {} start_y: {}'.format(current_interaction, coords['start_x'], coords['start_y']))
    else:
        print(
            '{} coordinates: start_x: {} start_y: {} end_x: {} end_y: {}'.format(current_interaction, coords['start_x'],
                                                                                 coords['start_y'], coords['end_x'],
                                                                                 coords['end_y']))


def calc_coordinates(current_app, current_interaction):
    width = info['width']
    height = info['height']

    if current_interaction == 'drawer':
        coords['start_x'] = int(width * 0)
        coords['start_y'] = int(height * 0.5)
        coords['end_x'] = int(width * 0.85)
        coords['end_y'] = int(height * 0.5)
        print_calculated_coords(current_interaction)

    elif current_interaction == 'close_drawer':
        coords['start_x'] = int(width * 0.7)
        coords['start_y'] = int(height * 0.5)
        coords['end_x'] = 0
        coords['end_y'] = 0

        print_calculated_coords('close_drawer')
        print('Wait after touch')

    elif current_interaction == 'switching_pages':
        if current_app == 'Android-native':
            button_x_factor = 0.29514
            button_y_factor = 0.3625
        elif current_app == 'Android-react':
            button_x_factor = 0.5
            button_y_factor = 0.4
        elif current_app == 'Android-flutter':
            button_x_factor = 0.5
            button_y_factor = 0.4
        elif current_app == 'Android-ionic':
            button_x_factor = 0.1
            button_y_factor = 0.15

        coords['start_x'] = int(button_x_factor * info["width"])
        coords['start_y'] = int(button_y_factor * info["height"])
        coords['end_x'] = 0
        coords['end_y'] = 0

        print_calculated_coords(current_interaction)

    elif current_interaction == 'list_swipe':
        coords['start_x'] = int(width * 0.4)
        coords['end_x'] = int(width * 0.4)
        coords['start_y'] = int(height * 0.7)
        coords['end_y'] = int(height * 0.3)
        print_calculated_coords(current_interaction)

    else:
        three_dots_native_x_factor = 0.71875
        three_dots_native_y_factor = 0.0469
        coords['start_x'] = int(three_dots_native_x_factor * info["width"])
        coords['start_y'] = int(three_dots_native_y_factor * info["height"])
        coords['end_x'] = 0
        coords['end_y'] = 0
        print_calculated_coords('transition')


def testcase_1_open_and_close_drawer(current_app, current_interaction, counter):
    print_header(current_interaction, counter)
    vc.swipe(coords['start_x'], coords['start_y'], coords['end_x'], coords['end_y'], 300)
    print('Wait after opening drawer with swipe: 3 sec')
    vc.sleep(3)
    calc_coordinates(current_app, 'close_drawer')
    vc.click(coords['start_x'], coords['start_y'])
    print('Wait after closing drawer with click: 3 sec')
    vc.sleep(3)


def testcase_2_switching_pages(current_interaction, counter):
    print_header(current_interaction, counter)
    vc.click(coords['start_x'], coords['start_y'])
    print('Wait after button touch for 4 sec')
    vc.sleep(4)


def testcase_3_list_swipe(current_interaction, counter):
    print_header(current_interaction, counter)
    vc.swipe(coords['start_x'], coords['start_y'], coords['end_x'], coords['end_y'], 400)
    print ('Wait after swipe for 4 sec')
    vc.sleep(4)


def transition_between_testcases(current_app, current_interaction):
    print ('~~~~~~~~~Change Activity~~~~~~~~~')
    if current_app == 'Android-native':
        calc_coordinates(current_app, 'transition')
        print("~~Click on three dots~~~")
        vc.click(coords['start_x'], coords['start_y'])
        print("Wait 3")
        time.sleep(3)
        print("~~~Click on Next Testcase~~~")
        vc.click(coords['start_x'], coords['start_y'])
        print("Wait 3")
        time.sleep(3)

    elif current_app == 'Android-react' or current_app == 'Android-ionic':
        if current_interaction == 'drawer':
            calc_coordinates(current_app, 'transition')
            print("~~Click on three dots~~~")
            vc.click(coords['start_x'], coords['start_y'])
            print("Wait 3")
            time.sleep(3)
        elif current_interaction == 'switching_pages':
            calc_coordinates(current_app, 'transition')
            print("~~Click~~~")
            vc.click(coords['start_x'], coords['start_y'])
            print("Wait 3")
            time.sleep(3)
        elif current_interaction == 'list_swipe':
            calc_coordinates(current_app, 'transition')
            print("~~Click~~~")
            vc.click(coords['start_x'], coords['start_y'])
            print("Wait 3")
            time.sleep(3)

    elif current_app == 'Android-flutter':
        if current_interaction == 'drawer':
            calc_coordinates(current_app, 'transition')
            print("~~Click on three dots~~~")
            vc.click(coords['start_x'], coords['start_y'])
            print("Wait 3")
            time.sleep(3)
            print("~~~Click on Next Testcase~~~")
            vc.click(coords['start_x'], coords['start_y'])
            print("Wait 3")
            time.sleep(3)
        elif current_interaction == 'switching_pages':
            calc_coordinates(current_app, 'transition')
            print("~~Click~~~")
            vc.click(coords['start_x'], coords['start_y'])
            print("Wait 3")
            time.sleep(3)
        elif current_interaction == 'list_swipe':
            calc_coordinates(current_app, 'transition')
            print("~~Click~~~")
            vc.click(coords['start_x'], coords['start_y'])
            print("Wait 3")
            time.sleep(3)


def runAll():
    print('Display Size Width: {} Height: {}'.format(info['width'], info['height']))

    for durchgang in range(1, 4):
        # Interaktion auswaehlen, solange welche vorhanden sind
        for n in range(0, len(interactions)):
            current_interaction = interactions[n]['name']

            # Apps auswaehlen, solange welche vorhanden sind
            for m in range(0, len(apps)):
                current_app = apps[m]['type']
                print('Starting App {}'.format(current_app))
                h.start_app(apps[m]['package'] + '/' + apps[m]['package'] + '.' + apps[m]['activity'])
                # sleep until app is started
                print('Wait until app is started 10')
                time.sleep(10)

                if current_interaction == 'list_swipe' and current_app == 'Android-flutter':
                    transition_between_testcases(current_app, 'drawer')
                    print('Wait 5')
                    time.sleep(5)
                    calc_coordinates(current_app, 'switching_pages')
                    vc.click(coords['start_x'], coords['start_y'])
                    print('Wait 5')
                    time.sleep(5)
                    transition_between_testcases(current_app, 'switching_pages')
                elif current_interaction == 'switching_pages':
                    print('Warte nach dem Start der App: Wait 5')
                    time.sleep(5)
                    transition_between_testcases(current_app, 'drawer')
                elif current_interaction == 'list_swipe':
                    print('Wait 5')
                    time.sleep(5)
                    transition_between_testcases(current_app, 'drawer')
                    print('Wait 5')
                    time.sleep(5)
                    transition_between_testcases(current_app, 'switching_pages')

                # Vmstat eigene Klasse, 20 Sekunden Recording Time
                vmstat = Vmstat(20,
                                'vmstat_{}_{}_{}_{}.txt'.format(serialno, current_app, current_interaction, durchgang))

                print('++++Number current threads before: {}'.format(threading.active_count()))

                # start performance metering
                print('Starting Performance Measurements')
                systrace_thread = threading.Thread(target=vmstat, name='perf-vmstat-thread')
                systrace_thread.start()
                print('++++Number current threads after: {}'.format(threading.active_count()))

                # sleep until metering is started
                print('Wait until performance measurements start: 3 sec')
                time.sleep(3)

                start = timeit.default_timer()
                if interactions[n]['name'] == 'drawer':
                    for o in range(1, interactions[n]['runs']):
                        calc_coordinates(current_app, current_interaction)
                        testcase_1_open_and_close_drawer(current_app, current_interaction, o)
                elif interactions[n]['name'] == 'switching_pages':
                    for o in range(1, interactions[n]["runs"]):
                        calc_coordinates(current_app, current_interaction)
                        testcase_2_switching_pages(current_interaction, o)
                elif interactions[n]["name"] == "list_swipe":
                    for o in range(1, interactions[n]["runs"]):
                        calc_coordinates(current_app, current_interaction)
                        testcase_3_list_swipe(current_interaction, o)

                print('Warte nach der Ausfuehrung der Interaktion 5 Sekunden')
                time.sleep(5)
                stop = timeit.default_timer()
                print('App: {} - Interaction: {} - Time: {}'.format(current_app, current_interaction, stop - start))

                ## Perf Meas Stop
                vmstat.pull_data(target_folder='/Users/paulaengelberg/Desktop/i/data/' + current_app + '/')
                print('Joining Thread')
                systrace_thread.join()
                print('++++Number current threads after join: {}'.format(threading.active_count()))

                # stop app
                print("Stopping App")
                h.stop_app(apps[m]["package"])

            print("Nach Durchlauf aller Apps Wait 5")
            time.sleep(5)


runAll()
csvcreator = csv.CsvCreator(PATH_DATA)
csvcreator.create_csv()
