import http
import httpx, json, utils, pyperclip

def validateToken(Token):
    r = httpx.get(
        "https://discord.com/api/v9/users/@me/guilds", 
        headers=utils.getHeaders(Token)
    )
    if r.status_code >= 200 and r.status_code < 300:
        return True
    else:
        return False

def validateGuild(Token, Guild):
    r = httpx.get(
        f"https://discord.com/api/v9/guilds/{Guild}",
        headers=utils.getHeaders(Token)
    )
    if r.status_code >= 200 and r.status_code < 300:
        return True
    else:
        return False

def Initiate(Token, TargetID, VictimID):

    Bots = ""
    RolesCollection = {}
    ChannelsCollection = {}

    # Clear the server #
    i = httpx.get(
    f"https://discord.com/api/v9/guilds/{TargetID}/channels",
    headers=utils.getHeaders(Token)
    )

    for channel in i.json():
        utils.DeleteChannel(Token, channel)

    i = httpx.get(
    f"https://discord.com/api/v9/guilds/{TargetID}/roles",
    headers=utils.getHeaders(Token)
    )

    for role in i.json():
        if role['name'] != '@everyone':
            utils.DeleteRole(Token, TargetID, role)

    # Get Guild General Data
    j = httpx.get(
    f"https://discord.com/api/v9/guilds/{VictimID}",
    headers=utils.getHeaders(Token)
    )

    GuildData = j.json()
    Gpayload = {}
    Gpayload['name'] = GuildData['name']
    Gpayload['default_message_notifications'] = GuildData['default_message_notifications']
    Gpayload['description'] = GuildData['description']
    Gpayload['explicit_content_filter'] = GuildData['explicit_content_filter']
    Gpayload['premium_progress_bar_enabled'] = GuildData['premium_progress_bar_enabled']
    Gpayload['verification_level'] = GuildData['verification_level']

    Tpayload = {}
    Tpayload['name'] = f"(Cloner Core) | {GuildData['name']}"
    Tpayload['description'] = ""

    # Scrape Channels & Roles
    r = httpx.get(
    f'https://discord.com/api/v9/guilds/{VictimID}/channels',
    headers=utils.getHeaders(Token)
    )

    s = httpx.get(
    f'https://discord.com/api/v9/guilds/{VictimID}/roles',
    headers=utils.getHeaders(Token)
    )

    Channels = r.json()
    Channels.sort(reverse=True, key=utils.SortByType)

    Roles = s.json()
    Roles.sort(reverse=True, key=utils.SortByPosition)

    utils.printCasual(f"(Cloner Core) | Scraped {len(Channels)} channels & {len(Roles)} roles")


    # Change New Guild Info
    httpx.patch(
    f"https://discord.com/api/v9/guilds/{TargetID}",
    headers=utils.getHeaders(Token),
    data=json.dumps(Gpayload)
    )
    utils.printCasual(f"(Cloner Core) | Changed basic guild info")

    for role in Roles:
        if role['managed'] == True and 'premium_subscriber' not in role['tags']:
            Bots += f"{role['name']}, "

    for role in Roles:
        if role['name'] == '@everyone':
            default = utils.getDefaultRole(TargetID)
            payload = json.dumps(role)
            q = httpx.patch(
            f"https://discord.com/api/v9/guilds/{TargetID}/roles/{default['id']}",
            headers=utils.getHeaders(Token),
            data=payload)
            RolesCollection[role['id']] = q.json()['id']
            utils.printCasual(f"(Cloner Core) | Edited role : everyone")
        else:
            role['icon'] = ""
            role['unicode_emoji'] = ""
            payload = json.dumps(role)
            q = httpx.post(f"https://discord.com/api/v9/guilds/{TargetID}/roles", 
            headers=utils.getHeaders(Token),
            data=payload)
            try:
                RolesCollection[role['id']] = q.json()['id']
            except Exception as e:
                continue
            utils.printCreate(f"(Cloner Core) | Created role : {q.json()['name']}")

    for channel in Channels:
        for perms in channel['permission_overwrites']:
            try:
                perms['id'] = RolesCollection[perms['id']]
            except Exception as e:
                continue
        if channel['parent_id'] != None:
            try:
                channel['parent_id'] = ChannelsCollection[channel['parent_id']]
            except Exception as e:
                continue
        channel['bitrate'] = 96000
        payload = json.dumps(channel)

        q = httpx.post(f"https://discord.com/api/v9/guilds/{TargetID}/channels", 
        headers=utils.getHeaders(Token),
        data=payload)
        try:
            ChannelsCollection[channel['id']] = q.json()['id']
        except Exception as e:
            continue
        utils.printCreate(f"(Cloner Core) | Created channel : {q.json()['name']}")

    if 'COMMUNITY' in GuildData['features']:
        Cpayload = {}
        Cpayload['features'] = ['COMMUNITY']
        Cpayload['verification_level'] = GuildData['verification_level']
        Cpayload['default_message_notifications'] = GuildData['default_message_notifications']
        Cpayload['explicit_content_filter'] = GuildData['explicit_content_filter']
        Cpayload['rules_channel_id'] = ChannelsCollection[GuildData['rules_channel_id']]
        Cpayload['public_updates_channel_id'] = ChannelsCollection[GuildData['public_updates_channel_id']]

        httpx.patch(
            f"https://discord.com/api/v9/guilds/{TargetID}",
            headers=utils.getHeaders(Token),
            data=json.dumps(Cpayload)
        )
        utils.printCasual("(Cloner Core) | Enabled Community")

    # Create Template

    p = httpx.post(
    f"https://discord.com/api/v9/guilds/{TargetID}/templates",
    headers=utils.getHeaders(Token),
    data=json.dumps(Tpayload)
    )
    TemplateData = p.json()

    utils.printCasual("(Cloner Core) | Created Template")

    Clipboard = ""
    Clipboard += f"(Cloner Result) | `{GuildData['name']}`\n\n(`Template Link`) | https://discord.new/{TemplateData['code']}\n"
    Clipboard += f"(`Avatar`) | https://cdn.discordapp.com/icons/{VictimID}/{GuildData['icon']}.webp?size=2048\n"
    Clipboard += f"(`Banner`) | https://cdn.discordapp.com/banners/{VictimID}/{GuildData['banner']}.webp?size=2048\n"
    Clipboard += f"(`Bot List`) | {Bots}"

    pyperclip.copy(Clipboard)
    utils.printCasual("(Cloner Core) | Clone finished, template copied to your clipboard | CTRL+V to paste it")
