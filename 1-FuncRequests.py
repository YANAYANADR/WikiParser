import re
import time
import asyncio
import aiohttp
async def get_links(url, amt=1):
    allLinks = [{url}]
    # check if 1<=amt<=5
    if not 1 <= amt <= 5:
        raise ValueError('Вложенность от 1 до 5')
    # check if url is correct
    if not 'wikipedia' in url:
        raise ValueError('Ссылка не википедия')
    # get wikipedia domain

    async with aiohttp.ClientSession() as session:
        # ok sry this is complicated but umm here
        try:
            for k in range(0, amt):
                print('cycle' + str(k))
                allLinks.append(set())
                for checked_link in allLinks[k].copy():

                    print('check = ' + checked_link)
                    if not 'wikipedia' in checked_link:
                        # raise ValueError('Ссылка не википедия')
                        continue
                    else:
                        wiki = checked_link.split('/')[2]
                    async with session.get(checked_link) as r:
                        preText =await r.text()
                    # ok we only get links from mw-content-text
                    text = preText[preText.find('<div id="mw-content-text" class="mw-body-content">')
                                   :preText.rfind('<div id="catlinks" class="catlinks" data-mw="interface">')]
                    # print(text)
                    for i in re.finditer('<a href="', text):
                        linkEnd = i.end() + text[i.end():].find('"')
                        link = text[i.end():linkEnd]
                        # filter out stuff
                        if '/w/index.php' in link or '.svg' in link or '.png' in link or '.jpg' in link or link.startswith(
                                '#'):
                            continue
                        if link.startswith('/wiki/'):
                            link = 'https://' + wiki + link
                        allLinks[k + 1].add(link)
                # remove all from prev parse
                if not k == 0:
                    allLinks[k + 1] = allLinks[k + 1] - allLinks[k]
            # ok now we search 4 original link
            for arr in allLinks[2:]:
                if url in arr:
                    # print(arr)
                    return True
            return False

        except:
            raise Exception('Неизвестная ошибка :(')
    #apparently needed 4 "graceful shutdown" idk
    await asyncio.sleep(0)


# the thing
inpLink = input("Ссылка\n")
if not inpLink:
    print('Ссылка пустая, исп. по умолчанию')
    inpLink = 'https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B5_%D0%BE%D0%B7%D0%B5%D1%80%D0%BE'
while True:
    try:
        inpAmt = int(input('Вложенность\n'))
        break
    except:
        continue
try:
    print(asyncio.run(get_links(inpLink,inpAmt)))
except Exception as e:
    print(f'Ошибка, {e}')
