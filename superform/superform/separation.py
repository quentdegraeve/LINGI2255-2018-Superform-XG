import re

#text = "Je Test, des. trucs! Et j'espère, que ça marche? correctement. hope is live. ah"
#text = "Mais vous savez, moi je ne crois pas qu'il y ait de bonne ou de mauvaise situation. Moi si je devais résumer ma vie, aujourd'hui avec vous, je dirais que c'est d\'abord des rencontres, des gens qui m'ont tendu la main peut-être à un moment où je ne pouvais pas, où j'étais seul chez moi. Et c'est assez curieux de se dire que les hasards, les rencontres forgent une destinée. Parce que quand on a le goût de la chose, quand on a le goût de la chose bien faite, le beau geste, parfois on ne trouve pas l'interlocuteur en face, je dirais le miroir qui vous aide à avancer. Alors ce n'est pas mon cas, comme je disais là, puique moi au contraire j'ai pu, et je dis merci à la vie, je lui dis merci, je chante la vie, je danse la vie, je ne suis qu'amour. Et finalement quand beaucoup de gens me disent aujourd'hui. Mais comment fais-tu pour avoir cette humanité ? Et bien je leur réponds très simplement, je leur dit : C\'est ce goût de l\'amour, ce goût donc, qui m\'a poussé aujourd\'hui à entreprendre une construction mécanique, mais demain qui sait ? Peut-être simplement à me mettre au service de la communauté, à faire le don, le don de soi."
text = "Mais vous savez, moi je ne crois pas qu'il y ait de bonne ou de mauvaise situation. Moi si je devais résumer ma vie, aujourd'hui avec vous, je dirais que c'est d\'abord des rencontres, des gens qui m'ont tendu la main peut-être à un moment où http://www.moodleuniversiteclouvain.be je ne pouvais pas, où j'étais seul chez moi. Et c'est assez curieux de se dire que les hasards, les rencontres forgent une destinée. Parce que quand on a le goût de la chose, quand on a le goût de la chose bien faite, le beau geste, parfois on ne trouve pas l'interlocuteur en face, je dirais le miroir qui vous aide à avancer. Alors ce n'est pas mon cas, comme je disais là, puisque moi au contraire j'ai pu, et je dis merci à la vie, je lui dis merci, je chante la vie, je danse la vie, je ne suis qu'amour. Et finalement quand beaucoup de gens me disent aujourd'hui. Mais comment fais-tu pour avoir cette humanité ? Et bien je leur réponds très simplement, je leur dit : C\'est ce goût de l\'amour, ce goût donc, qui m\'a poussé aujourd\'hui à entreprendre une construction mécanique, mais demain qui sait ? Peut-être simplement à me mettre au service de la communauté, à faire le don, le don de soi."


my_str = text
# Si on veut séparer suivant les mots et pas les phrases alors on rajoute le char : ' '

tweets = []
limit = 280

if len(text) <= limit:
    tweets += [text]
else:
    limit -= 4

    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    url_index = []
    url_len = []
    for url in urls:
        url_index.append(text.find(url))
        url_len.append(len(url))

    replacements = (',', '!', '?', ':', ';')
    for r in replacements:
        my_str = my_str.replace(r, '.')

    sentences = my_str.split(".")
    index = 0    # index général dans text
    nbTweet = 0  # nombre de tweets
    count = 0    # taille du tweet actuel
    temp = ""    # tweet temporaire
    for s in sentences:
        if (len(s)+1) > limit:
            print("sentence longer than limit")
            # cut between words
        else:
            if (count+len(s)+1) < limit:   # tweet assez petit ? +1 ?
                for (i, l) in zip(url_index, url_len):
                    if (i <= count <= i+l) or (i <= count+len(s) <= i+l):  # url in this part
                        if limit-count < l+i-index:  # pas assez place pour url
                            tweets += [temp]
                            if text[index] == ' ':
                                temp = text[index + 1: index + len(s) + 1]
                                count = len(s)
                            else:
                                temp = text[index: index + len(s) + 1]
                                count = len(s) + 1
                            nbTweet += 1

                temp += text[index: index+len(s)+1]
                count += len(s)+1
            else:                          # tweet trop grand
                tweets += [temp]
                if text[index] == ' ':
                    temp = text[index+1: index+len(s)+1]
                    count = len(s)
                else:
                    temp = text[index: index+len(s)+1]
                    count = len(s)+1
                nbTweet += 1
        index += len(s) + 1

if not len(tweets) == 1:
    for i in range(0, len(tweets)):
        tweets[i] = str(i+1) + '/' + str(len(tweets)) + ' ' + tweets[i]

for i in range(0, len(tweets)):
    print(tweets[i])
print()
print("size of tweets: ")
for i in range(0, len(tweets)):
    print(len(tweets[i]))










