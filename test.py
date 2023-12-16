string = "\CHAT pavan bhat"
if string.startswith("\CHAT"):
    tmp = string.split(" ")
    nick = " ".join(tmp[1:])
    print(nick)