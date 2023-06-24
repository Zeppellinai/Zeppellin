import json


def is_room(input: str):
    input = input.lstrip(" ").rstrip(" ")

    if input.isdigit() or input.lower() in ["mnž", "sp.s.", "aktų s."]: return True

    if input[:-1].isdigit():
        for tmp in ["...a", "...b"]:
            if tmp.replace("...", input[:-1]) == input.lower(): return True
    
    return False

def count_rooms(input: str):
    options = []
    last_idx = -1
    split_list = input.split()

    for idx, split in enumerate(split_list):
        if is_room(split):
            options.append(" ".join(split_list[last_idx+1:idx+1]))
            last_idx = idx

    return options
            



    
    # return ""

    # digits_found = 0
    # rooms_found = 0
    # indexes = []
    # for idx, c in enumerate(input): 
    #     if c.isdigit(): 
    #         digits_found += 1
            
    #         try:
    #             if input[idx + 1] in ["a", "b"] and input[idx + 2] == " ":
    #                 indexes.append(int(idx + 1))
    #         except IndexError:
    #             indexes.append(len(input) - 1)
    

    # if float(digits_found / 3).is_integer():
    #     rooms_found += digits_found / 3


    # else:
    #     print("Fix yo' code! Failed to parse: " + input)
    #     exit()

    # for special_room in ["Mnž", "Sp.s.", "Aktų s."]:
    #     rooms_found += input.count(special_room)
    

    
    # parts = [input[i:j] for i,j in zip(indexes, indexes[1:]+[None])]
    # print(parts)

    # return int(rooms_found), indexes


print(count_rooms("Anglų kalba 301a"))


# with open("2023-V2.json", encoding = 'utf-8') as f:
#     input = json.loads(f.read())

# for grade in [0]:
#     for weekday in input['7A']:
#         for lesson in input['7A'][weekday]:
#             lesson = str(lesson)
    
            # if lesson.count(",") > 0:
            #     for idx, split_lesson in enumerate(lesson.split(',')):
            #         split_lesson_name = ''.join([i for i in split_lesson if not is_room(i)]).lstrip(" ").rstrip(" ")
                    
            #         if idx == 0 and is_room(split_lesson.replace(split_lesson_name, "")):
            #             options = []
            #             options.append(split_lesson_name + " " + split_lesson.replace(split_lesson_name, "").lstrip(" "))
    
            #             for lesson_and_room_OR_room in lesson.split(",")[0+1:len(lesson.split(","))]:
            #                 lesson_and_room_OR_room = lesson_and_room_OR_room.lstrip(" ")
    
            #                 if is_room(lesson_and_room_OR_room): options.append(split_lesson_name + " " + lesson_and_room_OR_room)  
            #                 else: options.append(lesson_and_room_OR_room)
                            
#                         print(options)