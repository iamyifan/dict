import requests


class Dict:
    def __init__(self) -> None:
        self.prefix = 'https://api.dictionaryapi.dev/api/v2/entries/en/' 

    def build_url(self, word: str) -> str:
        """ Build the full URL by using the free API. """
        url = self.prefix + word 
        return url

    def retrieve_url(self, url: str) -> str:
        """ Return the retrieved information in JSON format. """
        r = requests.get(url)
        return r.json()

    def parse_json(self, json: str) -> str:
        blocks = []
        block = ''
        for p in json['phonetics']:
            if 'text' in p.keys():
                block += f"{p['text']} "
        block = block[:-1] + '\n'
        blocks.append(block)
        for m in json['meanings']:
            pos = m['partOfSpeech']
            block = ''
            for d in m['definitions']:
                block += f"[{pos}] def: {d['definition']}\n"
                if 'example' in d.keys():
                    block += " " * (len(pos) + 3) + f"eg: {d['example']}\n"
                if len(d['synonyms']) > 0:
                    tmp = ''
                    for s in d['synonyms']:
                        tmp += f'{s}; '
                    block += " " * (len(pos) + 3) + f"syn: {tmp[:-2]}\n"
                if len(d['antonyms']) > 0:
                    tmp = ''
                    for a in d['antonyms']:
                        tmp += f'{a}; '
                    block += " " * (len(pos) + 3) + f"ant: {tmp[:-2]}\n"
            blocks.append(block)
        return blocks

    def show_results(self, blocks: None | list[str]) -> None:
        res = ''
        if blocks != None:
            for b in blocks:
                res += b
        print(res)

    def search(self, word: str) -> None | str:
        url = self.build_url(word)
        json = self.retrieve_url(url)
        if type(json) == dict:
            return None
        else:
            return self.parse_json(json[0])


if __name__ == '__main__':
    d = Dict()
    while True:
        blocks = d.search(input('Search: '))
        d.show_results(blocks)
