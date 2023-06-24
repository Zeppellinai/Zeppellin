import time, requests, random

skip_list = ["PAMOKŲ PAKEITIMAI 2021 12 21", "PAMOKŲ PAKEITIMAI  PENKTADIENIUI 2021 12 17", "KETVIRTADIENIO (12.16) pamokų pakeitimai"] #for gods sake, can't scrape all msgs, because they used a diff date format a while back

def return_pass():
    return {"password": "no_pass", "username": "4_u"} #TODO: cry about it

def to_ascii(input: str):
    output = input
    for letters in {"ą": "a", "č": "c", "ę": "e", "ė": "e", "į": "i", "š": "s", "ų": "u", "ū": "u", "ž": "z"}.items(): output = output.replace(letters[0], letters[1])
    return output

def to_date(year: int, header: str):
    header = to_ascii(header)
    try:
        month_str = to_ascii(''.join([i for i in header.lower().split("ui, ")[1] if not i.isdigit()]).split("d.")[0].rstrip(" ").lstrip(" "))
    except:
        month_str = to_ascii(header.lower()).replace("pamoku pakeitimai ", "").split(" ")[0].replace(" ", "")

    day = int(header.split(month_str)[-1].replace(" ", "").split("d.")[0])
    months_dict = {"sausis": 1, "sausio": 1, "vasaris": 2, "vasario": 2, "kovas": 3, "kovo": 3, "balandis": 4, "balandzio": 4, "geguze": 5, "geguzes": 5, "birzelis": 6, "birzelio": 6, "liepa": 7, "liepos": 7, "rugpjutis": 8, "rugpjucio": 8, "rugsejo": 9, "rugsejio": 9, "rugsejis": 9, "spalis": 10, "spalio": 10, "lapkritis": 11, "lapkricio": 11, "gruodis": 12, "gruodzio": 12}
    
    for month in months_dict.items(): 
        if month_str == month[0]: month_int = month[1]

    return f"{year}-{month_int:02d}-{day:02d}"



last_login, last_req = 0, 0

def send_req(endpoint = '', data = {}):
    global last_login, last_req
    login = return_pass()
    server = 'http://127.0.0.1:5000/'

    if time.time() - last_login > 1200:
        print("No active session, logging in...")
        result = str(requests.post(server + "log_in", json = login).text).lstrip(" ").rstrip(" ") == ""
        last_login = time.time()
        time.sleep(5)
        if result: print("Logged in successfully!")
        if endpoint == '': return result
    
    if endpoint != '':
        delta = 5 + random.randint(-1, 4)
        time_between_last_req = time.time() - last_req or time.time() - delta
        if time_between_last_req < 5: print(f"Waiting {round(delta - time_between_last_req, 2)}s..."); time.sleep(delta - time_between_last_req)
        last_req = time.time()
        return requests.post(server + endpoint, json = data, cookies = login).json()
        

    



int_msgs = 0
msgs_page = 11
dates = []


while True:
    dumped_msgs = []
    msgs = send_req('pranesimai', {"puslapis": msgs_page})
    for msg in msgs["pranesimai"]:
        if "pakeitimai" in msg["tema"].lower():
            if msg["tema"] not in skip_list:
                print(f"Dumping: {msg['tema']}")
                msg_response = send_req("pranesimas", {"pranesimo id": msg["id"], "id": msgs["id"]})
                
                date = to_date(int(msg_response["data"].split("-")[0]), msg["tema"])
                if date in dates: date = date + "-DISCARDED"
                
                print(f"Date sent: {msg_response['data']}")

                with open(f"../data/reschedulings/{date}.txt", "w", encoding = 'utf-8') as f:
                    f.write(msg_response["html tekstas"])
                
                dates.append(date)

                int_msgs +=1
                print(f"Dumped MSGs: {int_msgs}, page: {msgs_page}")
                print("----------------------------------------------------")

    msgs_page += 1

