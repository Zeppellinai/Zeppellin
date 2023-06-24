from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date

import os, pyautogui, json

grades = []
timetable = []
lessons = {}

custom_names = {
    "(etika)": "Dorinis ugdymas [etika]",
    "tikyba": "Dorinis ugdymas [tikyba]"
}


def get_value():
    global driver
    return driver.find_element(by=By.CSS_SELECTOR, value='#formulaBarTextDivId_textElement > div').text

def reset_to_corner():
    for i in range(20): pyautogui.press('up'); pyautogui.press('left')

def scrape_all_grades():
    global grades

    reset_to_corner()
    for i in range(4): pyautogui.press('down')  #Jump to classes

    while True:
        grade = get_value().replace(' ', '')

        if grade != '':
            grades.append(grade)
            pyautogui.press('down')
        else:
            return grades

def scrape_timetable():
    global timetable

    reset_to_corner()

    pyautogui.press('down')
    pyautogui.press('right') 

    while True:
        value = get_value().replace('', '')

        if len(timetable) > 0: 
            if value == timetable[0]: break
        
        timetable.append(value)

        pyautogui.press('down')
        value = get_value().replace(' ', '')
        timetable.append(value)
        
        pyautogui.press('up')
        pyautogui.press('right')

def is_room(input: str):
    input = input.lstrip(" ").rstrip(" ").replace(",", "").replace(";", "")

    if input.isdigit() or input.lower() in ["mnž.", "sp.s.", "aktų s."]: return True

    if input[:-1].isdigit():
        for tmp in ["...a", "...b"]:
            if tmp.replace("...", input[:-1]) == input.lower(): return True
    
    return False

def parse_options(input: str):
    options = []
    last_idx = -1
    split_list = input.split()

    phase_1_done = False
    if input.count(",") > 0:
        for idx, split_lesson in enumerate(input.split(',')):
            split_lesson = split_lesson.rstrip(" ").lstrip(" ")
            split_lesson_name = ''.join([i for idx, i in enumerate(split_lesson) if not (i.isdigit() or i in ["a", "b"] and split_lesson[idx - 1].isdigit())]).lstrip(" ").rstrip(" ") #moment™ TODO: Make this accept special rooms ("mnž", "sp.s.", "aktų s.")
            
            if idx == 0 and is_room(split_lesson.replace(split_lesson_name, "")):
                options.append(split_lesson_name + " " + split_lesson.replace(split_lesson_name, "").lstrip(" "))

                print(input.split(",")[1:len(input.split(","))])
                for lesson_and_room_OR_room in input.split(",")[1:len(input.split(","))]:
                    lesson_and_room_OR_room = lesson_and_room_OR_room.lstrip(" ").rstrip(" ")

                    for __idx, _lesson_room in enumerate(lesson_and_room_OR_room.split(" ")):
                        if is_room(_lesson_room): options.append
                        elif _lesson_room.lower() == "aktų" and split_lesson.split(" ")[__idx + 1].lower() == "s.": room += "Aktų s."

        phase_1_done = True
    
    # elif input.count(";") > 0:
    #     for idx, split_lesson in enumerate(input.split(';')):
    #         split_lesson = split_lesson.rstrip(" ").lstrip(" ")

    #         room = ""
    #         for _idx, lesson_room in enumerate(split_lesson.split(" ")):
    #             if is_room(lesson_room): room += lesson_room
    #             elif lesson_room.lower() == "aktų" and split_lesson.split(" ")[_idx + 1].lower() == "s.": room += "Aktų s."
            
    #         lesson_name = split_lesson.replace(room, "").lstrip(" ").rstrip(" ")

    #         if idx == 0:
    #             options.append(split_lesson_name + " " + room.lstrip(" ").lstrip(" "))


    #             for lesson_and_room_OR_room in input.split(";")[1:len(input.split(";"))]:
    #                 lesson_and_room_OR_room = lesson_and_room_OR_room.lstrip(" ").rstrip(" ")
    #                 if is_room(lesson_and_room_OR_room): options.append(lesson_name + " " + lesson_and_room_OR_room)  
    #                 else: options.append(lesson_and_room_OR_room)

    #     phase_1_done = True

    if not phase_1_done:
        for idx, split in enumerate(split_list):
            if is_room(split) and not phase_1_done:
                options.append(" ".join(split_list[last_idx+1:idx+1]))
                last_idx = idx

    if len(options) < 2: return " ".join(split_list)

    return options

def scrape_all_lessons():
    global lessons
    j = 0

    while True:
        reset_to_corner()
        for i in range(4+j): pyautogui.press('down')  #Jump to classes
        j += 1
        
        grade = get_value().replace(' ', '').replace('\n', '')
        if grade == '': break
        lessons[grade] = {}

        for weekday in range(1, 6):
            lessons[grade][int(weekday)] = []
            for i in range(7):

                pyautogui.press('right')
                lesson = get_value().rstrip(' ').lstrip(' ')
                lessons[grade][int(weekday)].append(parse_options(lesson))



options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("start-maximized")

driver = webdriver.Chrome(options=options)
driver.get('https://jurguciomokykla365-my.sharepoint.com/:x:/g/personal/osvaldas_valiukas_jurguciomokykla_lt/EeND6pjg59pJjaVVbg_C_wwBShTcOnmxFDC2RRhMZLwynA')
driver.implicitly_wait(1)
frame_0 = driver.find_element(by=By.XPATH, value='/html/body/div[1]/iframe')
driver.switch_to.frame(frame_0)

scrape_all_lessons()

latest_ver = -1
for file in os.listdir('../data/timetables'):
    if file.endswith('.json'):
        file_ver = int(file.replace(str(date.today().year) + '-V', '').replace('.json', ''))
        if file_ver > latest_ver: latest_ver = file_ver

with open(f'../data/timetables/{date.today().year}-V{latest_ver + 1}.json', 'w', encoding='utf-8') as fp:
    json.dump(lessons, fp, ensure_ascii=False)