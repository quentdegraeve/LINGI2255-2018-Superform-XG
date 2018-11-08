import re
text = "Utile pour vos tweets sur Twitter vos messages texto SMS, vos dissertations, rédactions, essais nouvelles sdfqsdfqsdfqsdfqwdf articles et romans voici une calculatrice en ligne gratuite qui compte le nombre de caractères ou lettres dans un texte hdhdhdhdhdhdhd jamlkjqsdmflkj fqmslkj www.moodleucl.uclouvain.be  Journalistes, écrivains, étudiants, chercheurs www.google.co.uk , demandeurs d'emploi: utilisez cet outil gratuit pour compter le nombre de lettres ou caractères de votre document que ce soit un curriculum vitae, une brochure, une lettre de candidature, une thèse, un doctorat, un travail de recherche, ou autres devoirs - que vous les écriviez sur votre tablette ou portable Apple Ipad Air, Iphone, Android Samsung Galaxy, Sony Xperia, LeNovo IdeaTab, Archos, voire votre ordinateur Dell, Lenovo Yoga, Microsoft, HP ou MacBook. "
separators = (',', '!', '?', ':', ';', '\n')

my_str = text

tweets = []
limit = 280

if len(text) <= limit:
    tweets += [text]
else:
    limit -= 4
    urls = re.findall(r'((?:http[s]?:/{2})?(?:w{3}\.)?(?:\w+\.)+(?:com|fr|be|io|gov|net|tv|uk|ch|de|nl|lu)(?:/[^\s]+)?)', text)
    url_index = []
    url_len = []
    for url in urls:
        url_index.append(text.find(url))
        url_len.append(len(url))

    for sep in separators:
        my_str = my_str.replace(sep, '.')

    sentences = my_str.split(".")
    index = 0  # index général dans text
    nbTweet = 0  # nombre de tweets
    count = 0  # taille du tweet actuel
    temp = ""  # tweet temporaire

    for s in sentences:
        if (len(s) + 1) > limit:
            if separators == ' ':
                print("Split between characters")
                print([text[i:i+280] for i in range(0, len(text), 280)])
            else:
                print("Split between words")
        else:
            if not url_index:  # si pas d'url
                if (count + len(s) + 1) < limit:  # tweet small enough
                    temp += text[index: index + len(s) + 1]
                    count += len(s) + 1
                    index += len(s) + 1
                else:
                    tweets += [temp]
                    if text[index] == ' ':
                        temp = text[index + 1: index + len(s) + 1]
                        count = len(s)
                        index += len(s) + 1
                    else:
                        temp = text[index: index + len(s) + 1]
                        count = len(s) + 1
                        index += len(s) + 1
                    nbTweet += 1
            else:  # si url
                for (i, l) in zip(url_index, url_len):

                    print(s)
                    print(index)
                    if (i <= index <= i + l) or (i <= index + len(s) + 1 <= i + l):
                        # url in this part
                        if limit - count <= l + i - index + 1:  # no room in this tweet to add until end of url
                            if limit - count <= l + i:  # no room to add until start of url then start a new one
                                tweets += [temp]
                                nbTweet += 1
                                count = 0
                                temp = ""
                            else:  # enough room in this tweet to add until start of url
                                temp += text[index: i]
                                tweets += [temp]
                                nbTweet += 1
                                index += len(s) + 1
                                temp = text[i: index]  # start of a new tweet
                                count = index - i
                        else:  # url can be put in full in this tweet
                            if len(s) > limit - count:
                                # full sentence can't be put in this tweet, so take until end of url, then start new one
                                temp += text[index: i + l]
                                tweets += [temp]
                                nbTweet += 1
                                temp = text[i + l + 1: index + len(s) + 1]
                                index += len(s) + 1
                                count = index - i
                            else:
                                temp += text[index: index + len(s) + 1]
                                count += len(s) + 1
                                index += len(s) + 1

                    else:
                        # url not in this part
                        if (count + len(s) + 1) < limit:  # tweet small enough to put a sentence
                            temp += text[index: index + len(s) + 1]
                            count += len(s) + 1
                            index += len(s) + 1
                        else:  # tweet too big
                            tweets += [temp]
                            if text[index] == ' ':
                                temp = text[index + 1: index + len(s) + 1]
                                count = len(s)
                                index += len(s) + 1
                            else:
                                temp = text[index: index + len(s) + 1]
                                count = len(s) + 1
                                index += len(s) + 1
                            nbTweet += 1

    tweets += [temp]

if not len(tweets) == 1:
    for i in range(0, len(tweets)):
        tweets[i] = str(i + 1) + '/' + str(len(tweets)) + ' ' + tweets[i]

for t in tweets:
    print(t)
    print(len(t))
