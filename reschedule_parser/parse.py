from rich import print
from rich.pretty import pprint
import json, requests, time

_abc_classes = ["a", "b", "c", "d", "e", "f", "g"]  # must be lower-case
_123_classes = ["5", "6", "7", "8"]
changes = {}


def starts_with_class(input: str):
    input = input.lstrip(" ")

    if input[0] not in _123_classes or not input[1].lower() in _abc_classes:
        return False

    return True

def wrap_class(input: str):
    input = input.lstrip(" ").rstrip(" ")

    for i, char in enumerate(input):
        if char.isdigit() and input[i:i+3].isdigit(): return input.replace(input[i:i+3], f"[{input[i:i+3]}]")


print(wrap_class('206'))
exit()

with open("../data/reschedulings/2023-03-06.txt", "r", encoding="utf-8") as f: 
    text = f.read()
    text = text.replace("</p>", "\n").replace("<p>", "")
    if text.split("\n")[0].lower().count(" pakeit") > 0:
        text = text.replace(text.split("\n")[0] + "\n", "")

    text = text.split("<strong>")

    for change in text:
        if len(change) > 1 and change[0].isdigit() and change[1] == "p":

            lesson_idx = int(change[0])

            lessons_changes = change.split('</strong>')[1].lstrip(' ')
            lessons_changes = list(
                filter(lambda k: k != '', lessons_changes.split('\n')))

            # Yeah, I'm aware that I *should* be using ``lesson_change in lessons_changes``, but this is to support multi-class changes (Ex. 8b, 8c nebus)
            for lesson_change_idx in range(len(lessons_changes)):
                lesson_change = lessons_changes[lesson_change_idx]

                if lesson_change.count(",") > 0:

                    grades_affected = []
                    change = ""

                    for idx, grade_and_or_change in enumerate(lesson_change.split(",")):
                        grade_and_or_change = grade_and_or_change.lstrip(" ")

                        if len(grade_and_or_change) == 2 and starts_with_class(grade_and_or_change):
                            grades_affected.append(grade_and_or_change[0:2])

                        elif len(grade_and_or_change) > 2 and starts_with_class(grade_and_or_change):
                            grades_affected.append(grade_and_or_change[0:2])
                            change += grade_and_or_change[2:].lstrip(" ")

                        else:
                            change += ", " + grade_and_or_change.lstrip(" ")

                    if change.replace(" ", "") != "":
                        for affected_grade in grades_affected:
                            if not affected_grade in changes.keys():
                                changes[affected_grade] = {}
                            
                            
                            if lesson_idx in changes[affected_grade]:
                                if type(changes[affected_grade][lesson_idx]) == str:
                                    changes[affected_grade][lesson_idx] = [changes[affected_grade][lesson_idx]]
                                                                
                                changes[affected_grade][lesson_idx] = changes[affected_grade][lesson_idx].append(change.lstrip(" "))   
                            else:
                                changes[affected_grade][lesson_idx]  = change.lstrip(" ")

                    

                elif len(lesson_change) > 1 and starts_with_class(lesson_change):

                    grade = lesson_change[0:2].lower()
                    if not grade in changes.keys():
                        changes[grade] = {}
                    
                    if lesson_idx in changes[grade] and type(changes[grade][lesson_idx]) == str:
                        changes[grade][lesson_idx] = [changes[grade][lesson_idx]]
                        changes[grade][lesson_idx].append(lesson_change.removeprefix(grade).lstrip(" "))
                    else:
                        changes[grade][lesson_idx] = lesson_change.removeprefix(grade).lstrip(" ")



                    
    pprint(changes)





# for msg in msgs:
    

# from difflib import SequenceMatcher

# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()
