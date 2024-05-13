import re
import asyncio
import aiohttp


async def get_links(url, amt=1):
    all_links = [{url}]
    # Check if 1<=amt<=5
    if not 1 <= amt <= 5:
        raise ValueError('Вложенность от 1 до 5')
    # Check if url is correct
    if 'wikipedia' not in url:
        raise ValueError('Ссылка не википедия')
    async with aiohttp.ClientSession() as session:
        try:
            for k in range(0, amt):
                print('cycle' + str(k))
                all_links.append(set())
                for checked_link in all_links[k].copy():

                    print('check = ' + checked_link)
                    if 'wikipedia' not in checked_link:
                        continue
                    else:
                        wiki = checked_link.split('/')[2]
                    async with session.get(checked_link) as r:
                        preText = await r.text()
                    # Only get links from mw-content-text
                    text = preText[preText.find('<div id="mw-content-text" class="mw-body-content">')
                                   :preText.rfind('<div id="catlinks" class="catlinks" data-mw="interface">')]
                    for i in re.finditer('<a href="', text):
                        linkEnd = i.end() + text[i.end():].find('"')
                        link = text[i.end():linkEnd]
                        # filter out stuff
                        if '/w/index.php' in link or '.svg' in link or '.png' in link or '.jpg' in link or link.startswith(
                                '#'):
                            continue
                        if link.startswith('/wiki/'):
                            link = 'https://' + wiki + link
                        all_links[k + 1].add(link)
                # Remove all from prev parse
                if not k == 0:
                    all_links[k + 1] = all_links[k + 1] - all_links[k]
            # Search 4 original link
            for arr in all_links[2:]:
                if url in arr:
                    # print(arr)
                    return True
            return False

        except:
            raise Exception('Неизвестная ошибка :(')
    # "graceful shutdown"
    await asyncio.sleep(0)


inpLink = input("Ссылка\n")
if not inpLink:
    print('Ссылка пустая, исп. по умолчанию')
    inpLink = ('https://ru.wikipedia.org/wiki/'\
               '%D0%9F%D0%BE%D0%B4%D0%B1%D0%BE%D1%80%D0%BE%D0%B2%D1%81%D0%BA%D0%B'\
               'E%D0%B5_%D0%BE%D0%B7%D0%B5%D1%80%D0%BE')
while True:
    try:
        inpAmt = int(input('Вложенность\n'))
        break
    except:
        continue
try:
    print(asyncio.run(get_links(inpLink, inpAmt)))
except Exception as e:
    print(f'Ошибка, {e}')
