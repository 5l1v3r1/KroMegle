import requests, json, string, enum
from random import choice

class Event(enum.Enum):
    SEARCHING = 0
    CONNECTED = 1
    GOTMESSAGE = 2
    STRANGERDISCONNECTED = 3
    TYPING = 4
    SLEEP = 5
    COMMONLIKES = 6
    SERVERMSG = 7
    ERROR = 8
    CONNECTIONDIED = 9
    ANTINUDEBANNED = 10

class Variables:
    peoplecount = 0
    antinudeservers = []
    servers = []
    server = None
    clientid = None
    randid = None

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-US;q=0.6,en;q=0.4',
        'DNT': '1',
        'Host': '',
        'Origin': 'https://www.omegle.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
    }

    topics = [ ]

def genId():
    chars = (string.digits + string.ascii_uppercase).replace('I', '').replace('O', '')
    return ''.join(choice(chars) for _ in range(8))

def getStatus():
    re = requests.get(f'https://omegle.com/status??nocache=0.766924951633927&randid={Variables.randid}').text
    return json.loads(re)

def startChat():
    response = requests.post(f'https://{Variables.server}.omegle.com/start?caps=recaptcha2,t&firstevents=1&spid=&randid={Variables.randid}'+(f'''&topics=["{'", "'.join(Variables.topics)}"]''' if len(Variables.topics) > 0 else '')+'&lang=en')
    Variables.clientid = json.loads(response.text)['clientID']

def stopChat():
    response = requests.post(f'https://{Variables.server}.omegle.com/disconnect', data={'id': Variables.clientid})
    if response.status_code == 200 and 'win' in response.text.lower(): return True
    else: return False

def getEvent():
    event = json.loads(requests.post(f'http://{Variables.server}.omegle.com/events', data={'id': Variables.clientid}).text)

    if event != None:
        opcode = event[0][0].lower()
        if opcode == 'waiting': return (Event.SEARCHING, None)
        elif opcode == 'connected': return (Event.CONNECTED, None)
        elif opcode == 'gotmessage': return (Event.GOTMESSAGE, event[0][1])
        elif opcode == 'strangerdisconnected': return (Event.STRANGERDISCONNECTED, None)
        elif opcode == 'typing': return (Event.TYPING, None)
        elif opcode == 'commonlikes': return (Event.COMMONLIKES, event[0][1:])
        elif opcode == 'servermessage': return (Event.SERVERMSG, event[0][1])
        elif opcode == 'error': return (Event.ERROR, event[0][1])
        elif opcode == 'connectiondied': return (Event.CONNECTIONDIED, None)
        elif opcode == 'antinudebanned': return (Event.ANTINUDEBANNED, None)
        else: return (Event.SLEEP, None)
    else:
        return (Event.SLEEP, None)

def sendMessage(msg):
    requests.post(f'http://{Variables.server}.omegle.com/typing', data={'id': Variables.clientid})
    req = requests.post(f'http://{Variables.server}.omegle.com/send', data={'msg': msg, 'id': Variables.clientid})
    requests.post(f'http://{Variables.server}.omegle.com/stoppedtyping', data={'id': Variables.clientid})
    if req.status_code == 200 and 'win' in req.text.lower(): return True
    else: return False

def initModule():
    info = getStatus()
    Variables.peoplecount = info['count']
    Variables.antinudeservers = info['antinudeservers']
    Variables.servers = info['servers']

    server = choice(info['servers'])
    Variables.server = server
    Variables.headers['Host'] = f'{server}.omegle.com'
    Variables.randid = genId()

initModule()