#!/usr/bin/env python3

import socket
import json
import random
import argparse
import ssl

# Establishes our arguments
# Since the default value of the port depens on whether or not we use TLS encryption,
# I didn't assign a default here
parser = argparse.ArgumentParser()
parser.add_argument('-p', type=int)
parser.add_argument('-s', action='store_true')
parser.add_argument('hostname')
parser.add_argument('northeastern_username')
args = parser.parse_args()
port = args.p

# Creates our connection to the server
# This handles our TLS encryption logic and gives our port a proper default value
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = socket.gethostbyname(args.hostname)
if (args.s):
    s = ssl.wrap_socket(s)
    if (port == None):
        port = 27994
elif (port == None):
    port = 27993
s.connect((host_ip, port))

# sendMsg: json -> json
# Accepts a message as a json object, sends it, and returns the respone as a json object
# To avoid cutting off the reponse, continuously read and append buffers until we hit a newline,
# then discard everything after the newline and return the buffer. If we read 50 buffers without
# a newline, we assume something went wrong and kill the program. Likewise, if we get an error back
# report it and kill.
def sendMsg(message):
    s.send(message.encode())
    count = 0
    message = ""
    while(not("\n" in message)):
        message += s.recv(4096).decode()
        count += 1
        if (count >= 50): # 50 is completely arbitrary and probably overkill
            print("Connection terminated after 50 failed attempts")
            exit()
    response = json.loads(message.split("\n", 1)[0])
    if (response["type"] == "error"):
        print('Server returned error: ' + response["message"])
        exit()
    return response

# Sends our hello to the server using the username from our args and records the id for future messages
myId = sendMsg(json.dumps({"type": "hello", "northeastern_username": args.northeastern_username}) + "\n")["id"]

# updateWordList: json{string, int[]} string[] -> string[]
# Updates the given word list with the information in the given guess
# The unknown list tells us what indicies we haven't figured out yet to avoid repeatedly filtering
# for the same solved character.
unknown = [*range(5)]
def updateWordList(guess, wordList):
    global unknown
    word = guess["word"]
    marks = guess["marks"]
    for i in unknown:
        if (marks[i] == 2):
            wordList = list(filter(lambda x: word[i] == x[i], wordList))
        elif (marks[i] == 1):
            wordList = list(filter(lambda x: ((word[i] in x) and not(word[i] == x[i])), wordList))
    unknown = list(filter(lambda x: marks[x] != 2, unknown))
    return wordList

# Gets our word list from the appropraite file
wordList = open('wordlist.txt').readlines()

# This is the main body of our wordle program. While we have words left to guess, pick a random one
# to remove from the list and submit as a guess. If we get a "bye", print the flag and kill the program.
# Otherwise, update the word list with our new information and try again.
while (len(wordList) > 0):
    word = random.choice(wordList).replace("\n", "")
    wordList.remove(word + "\n")
    response = sendMsg(json.dumps({"type": "guess", "id": myId, "word": word}) + "\n")
    if (response["type"] == "bye"):
        print(response["flag"])
        exit()
    wordList = updateWordList(response["guesses"][-1], wordList)

# Just in case :)
print("Word list has no elements remaining")
