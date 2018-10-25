import re


def tweet_split(text, separators):
    my_str = text

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

        for sep in separators:
            my_str = my_str.replace(sep, '.')

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
                if (count+len(s)+1) < limit:   # tweet small enough
                    if not url_index:  # ok
                        temp += text[index: index + len(s) + 1]
                        count += len(s) + 1
                        index += len(s) + 1
                    else:
                        for (i, l) in zip(url_index, url_len):
                            if (i <= index <= i + l) or (i <= index + len(s) + 1 <= i + l):  # url in this part
                                if limit - count < l + i - index:  # no room in this tweet to put entire url
                                    temp += text[index: i]
                                    tweets += [temp]
                                    nbTweet += 1
                                    index += len(s) + 1
                                    temp = text[i: index]  # start of a new tweet
                                    count = index-i
                                else:
                                    temp += text[index: index + len(s) + 1]
                                    count += len(s) + 1
                                    index += len(s) + 1
                            else:  # url not in this part
                                temp += text[index: index + len(s) + 1]
                                count += len(s) + 1
                                index += len(s) + 1

                else:                          # tweet too big
                    tweets += [temp]
                    if text[index] == ' ':
                        temp = text[index+1: index+len(s)+1]
                        count = len(s)
                        index += len(s) + 1
                    else:
                        temp = text[index: index+len(s)+1]
                        count = len(s)+1
                        index += len(s) + 1
                    nbTweet += 1
        tweets += [temp]

    if not len(tweets) == 1:
        for i in range(0, len(tweets)):
            tweets[i] = str(i+1) + '/' + str(len(tweets)) + ' ' + tweets[i]

    """
    for i in range(0, len(tweets)):
        print(tweets[i])
    print()
    print("size of tweets: ")
    for i in range(0, len(tweets)):
        print(len(tweets[i]))
    """










