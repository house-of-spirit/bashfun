import string
import hashlib
import random
import sys

# valid variable names have the regex [a-zA-Z_][a-zA-Z0-9_]+
rand_string = lambda x: random.choice(string.ascii_letters + "_") + ''.join([random.choice(string.ascii_letters + string.digits + "_") for y in range(x-1)])

def payload_init():
    
    # n is the accumulator, p the final payload
    assoc = {k:rand_string(2) for k in string.hexdigits[:-6].lower() + 'np'}
    payload = ""

    for k,v in assoc.items():
        payload += "{}={};".format(v,k)

    payload += "{}='';{}='';".format(assoc['n'], assoc['p'])

    return assoc, payload

def create_payload_for_char(char, assoc):
    
    a = 0
    b = 0
    index = 0

    while True:
        a = hashlib.sha1()
        a.update(rand_string(16).encode())
        a = a.hexdigest()
        b = hex(ord(char))[2:]
        
        if len(b) == 1:
            b = '0' + b       
 
        if b in a:
            index = a.index(b)
            break

    payload = "{}={};".format(assoc['n'], ''.join(['$' + assoc[x] for x in a]))
    payload += "{0}=\"${0}".format(assoc['p'])
    payload += "\\x${" + assoc['n'] + ":{}:2".format(index) + "}\";" + "{}='';".format(assoc['n'])
     
    return payload
    
    
def main():
    
    payload = open(sys.argv[1]).read()
    
    init = payload_init() 
    while True:
        if len(list(init[0].values())) == len(set(list(init[0].values()))):
            break
    
    accumulator = list(init[0].values())[16]
    

    new_payload = init[1]
    
    for x in payload:
        new_payload += create_payload_for_char(x, init[0])
    new_payload += "$(printf ${});".format(init[0]['p'])
    print(new_payload)

main()
