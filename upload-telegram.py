from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
import os
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

rootPath = input("Informe o caminho da pasta onde o(s) arquivo(s) estão: ")
listaRootPath = os.listdir(rootPath)
api_id = int(input("Informe o api_id: "))
api_hash = input("Informe o api_hash: ")
chann = int(input("Informe o id do canal: "))

for folder in listaRootPath:
    rootPath = os.path.normcase(rootPath) + "\\"    
    path = rootPath + folder
    path = os.path.normcase(path) + "\\"
    tag = path.split("\\")
    tag = tag[-2:-1]
    tag = str(tag)
    tag = tag[2:-2]
    tag = tag.upper()
    tag = "#" + tag
    arquivos = os.listdir(path)
    # The first parameter is the .session file name (absolute paths allowed)
    with TelegramClient('anon', api_id, api_hash) as client:
        for file in arquivos:
            extensao = os.path.splitext(file)
            cap = file[:-len(extensao[1])]        
            print(cap)
            if extensao == ".mp4":
                metadata = extractMetadata(createParser(path + file))
                client.loop.run_until_complete(client.send_file(
                    chann,
                    path + file,
                    caption=cap + "\n" + tag,
                    attributes=(DocumentAttributeVideo(
                        (0,
                        metadata.get('duration').seconds)[metadata.has('duration')],
                        (0, metadata.get('width'))[metadata.has('width')],
                        (0, metadata.get('height'))[metadata.has('height')],
                        supports_streaming=1),
                        )
                    )
                )
            else:
                client.loop.run_until_complete(client.send_file(
                    chann,
                    path + file,
                    caption=cap + "\n" + tag,)
                )