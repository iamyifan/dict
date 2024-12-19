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
        block += '\n'
        blocks.append(block)

        for m in json['meanings']:
            pos = m['partOfSpeech']
            block = ''
            for d in m['definitions']:
                block += f"[{pos}] {d['definition']}\n"
                if 'example' in d.keys():
                    block += " " * (len(pos) + 3) + f"example: {d['example']}\n"
                if len(d['synonyms']) > 0:
                    block += " " * (len(pos) + 3) + f"synonyms: {d['synonyms']}\n"
                if len(d['antonyms']) > 0:
                    block += " " * (len(pos) + 3) + f"antonyms: {d['antonyms']}\n"
            blocks.append(block)
        return blocks

    def show_results(self, blocks: list[str]) -> None:
        for b in blocks:
            print(b)

    def search(self, word: str) -> None:
        url = self.build_url(word)
        json = self.retrieve_url(url)[0]
        blocks = self.parse_json(json)
        self.show_results(blocks)


if __name__ == '__main__':
    d = Dict()
    while True:
        d.search(input('Search: '))
