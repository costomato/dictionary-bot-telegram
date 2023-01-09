import requests

def search_word(word):
    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    data = requests.get(url + word).json()

    if type(data) is not list:
        return None

    result = ''
    count = 1
    for i in data:
        result += str(count) + '. *' + i['word'] + '*\n'
        if 'phonetic' in i:
            result += i['phonetic'] + '\n\n'
        for j in i['meanings']:
            if 'partOfSpeech' in j:
                result += '_' + j['partOfSpeech'] + '_\n'
            for k in j['definitions']:
                result += '-> ' + k['definition'] + '\n'
                if 'synonyms' in k and k['synonyms']:
                    result += '`Synonyms: ' + ', '.join(k['synonyms']) + '`\n'
                if 'antonyms' in k and k['antonyms']:
                    result += '`Antonyms: ' + ', '.join(k['antonyms']) + '`\n'
                if 'example' in k and k['example']:
                    result += '`Example: ' + k['example'] + '`\n'
            result += '\n'
        result += '\n'
        count += 1

    return result