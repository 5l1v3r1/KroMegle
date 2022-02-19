import time, os
from wrapper import *

Variables.topics = [
    'hacking',
    'hack',
    'cybersecurity',
]

continue_chat, idle = True, 0

while 1:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('KroMegle initalized.')
    startChat()
    if sendMessage('hello, i am KroMegle, a omegle bot written by Nexus. You can find me here -> https://github.com/Nexuzzzz/KroMegle. Have a nice day!'): print('>> Message sent.')
    while continue_chat:
        if idle > 5: print('>> Conversation timed out x_x'); stopChat(); continue_chat=False
        try:
            event = getEvent()

            if event[0] == Event.SEARCHING: print('>> Looking for people to talk to.')
            elif event[0] == Event.CONNECTED: print('>> Found stranger.')
            elif event[0] == Event.GOTMESSAGE: print(f'>> Stranger said: {event[1]}')
            elif event[0] == Event.TYPING: print('>> Stranger is typing...')
            elif event[0] == Event.STRANGERDISCONNECTED: print('>> Stranger disconnected. :('); continue_chat=False
            elif event[0] == Event.SLEEP: time.sleep(2); idle+=1
            else: print(f'>> Unrecognized event: {str(event)}')
        except KeyboardInterrupt: continue_chat=False
    
    if 'y' in input('>> Want to chat again? ').lower(): continue_chat=True; pass
    else: print('>> Bye!'); break