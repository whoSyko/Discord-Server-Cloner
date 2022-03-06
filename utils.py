import httpx
from colorama import Fore

def printDelete(msg):
    print(f"{Fore.RED}{msg}{Fore.RESET}")

def printCasual(msg):
    print(f"{Fore.LIGHTBLUE_EX}{msg}{Fore.RESET}")

def printCreate(msg):
    print(f"{Fore.LIGHTGREEN_EX}{msg}{Fore.RESET}")

def getDefaultRole(GuildId):
    q = httpx.get(
      f'https://discord.com/api/v9/guilds/{GuildId}/roles',
      headers={'Authorization': 'mfa.L_rSV10ph3XCTMYu98SOYw5xRrImGo5GK_nT8nN40mSaW4aThJNMWntabeDJHS_GupmruofYseEXLSWpI3JH'}
    )
    for role in q.json():
      if(role['name'] == '@everyone'):
        return role

def getHeaders(token):
    headers = {
      'Authorization': token,
      'Content-Type': 'application/json'
    }
    return headers

def SortByType(channel):
    if channel['type'] > 4:
        return 0
    else:
        return channel['type']

def SortByPosition(role):
    return role['position']

def DeleteChannel(Token, channel):
    httpx.delete(
        f"https://discord.com/api/v9/channels/{channel['id']}",
        headers=getHeaders(Token)
    )
    printDelete(f"(Cloner Cleaner) | Deleted Channel : {channel['name']}")

def DeleteRole(Token, guild, role):
    httpx.delete(
        f"https://discord.com/api/v9/guilds/{guild}/roles/{role['id']}",
        headers=getHeaders(Token)
    )
    printDelete(f"(Cloner Cleaner) | Deleted Role : {role['name']}")
