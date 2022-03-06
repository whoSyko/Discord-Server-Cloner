import core, fade, utils

Banner = """

 ▄████▄   ██▓     ▒█████   ███▄    █ ▓█████  ██▀███      ▄████▄   ▒█████   ██▀███  ▓█████ 
▒██▀ ▀█  ▓██▒    ▒██▒  ██▒ ██ ▀█   █ ▓█   ▀ ▓██ ▒ ██▒   ▒██▀ ▀█  ▒██▒  ██▒▓██ ▒ ██▒▓█   ▀ 
▒▓█    ▄ ▒██░    ▒██░  ██▒▓██  ▀█ ██▒▒███   ▓██ ░▄█ ▒   ▒▓█    ▄ ▒██░  ██▒▓██ ░▄█ ▒▒███   
▒▓▓▄ ▄██▒▒██░    ▒██   ██░▓██▒  ▐▌██▒▒▓█  ▄ ▒██▀▀█▄     ▒▓▓▄ ▄██▒▒██   ██░▒██▀▀█▄  ▒▓█  ▄ 
▒ ▓███▀ ░░██████▒░ ████▓▒░▒██░   ▓██░░▒████▒░██▓ ▒██▒   ▒ ▓███▀ ░░ ████▓▒░░██▓ ▒██▒░▒████▒
░ ░▒ ▒  ░░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░   ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░░ ▒░ ░
  ░  ▒   ░ ░ ▒  ░  ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ░  ░  ░▒ ░ ▒░     ░  ▒     ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░  ░
░          ░ ░   ░ ░ ░ ▒     ░   ░ ░    ░     ░░   ░    ░        ░ ░ ░ ▒    ░░   ░    ░   
░ ░          ░  ░    ░ ░           ░    ░  ░   ░        ░ ░          ░ ░     ░        ░  ░
░                                                       ░                      s y k o x ░
"""
print(fade.brazil(Banner))

Token = ""
TargetID = ""
VictimID = ""

Token = input("(Cloner Logger) | Token : ")

if core.validateToken(Token) == False:
  utils.printDelete("(Cloner Error) | Invalid Token")
else:
  # Valid Token, Go for guild Id
  VictimID = input("(Cloner Logger) | Guild Id to copy : ")
  if core.validateGuild(Token, VictimID) == False:
    utils.printDelete("(Cloner Error) | Invalid Guild Id")
  else:
    # Valid Token, target id, go for guild Id
    TargetID = input("(Cloner Logger) | Guild Id where to copy : ")
    if core.validateGuild(Token, TargetID) == False:
      utils.printDelete("(Cloner Error) | Invalid Guild Id")
    else:
      core.Initiate(Token, TargetID, VictimID)
