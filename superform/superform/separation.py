from math import ceil

#text = "Je Test, des. trucs! Et j'espère, que ça marche? correctement. hope is live. ah"
text = "Mais vous savez, moi je ne crois pas qu'il y ait de bonne ou de mauvaise situation. Moi si je devais résumer ma vie, aujourd'hui avec vous, je dirais que c'est d\'abord des rencontres, des gens qui m'ont tendu la main peut-être à un moment où je ne pouvais pas, où j'étais seul chez moi. Et c'est assez curieux de se dire que les hasards, les rencontres forgent une destinée. Parce que quand on a le goût de la chose, quand on a le goût de la chose bien faite, le beau geste, parfois on ne trouve pas l'interlocuteur en face, je dirais le miroir qui vous aide à avancer. Alors ce n'est pas mon cas, comme je disais là, puique moi au contraire j'ai pu, et je dis merci à la vie, je lui dis merci, je chante la vie, je danse la vie, je ne suis qu'amour. Et finalement quand beaucoup de gens me disent aujourd'hui. Mais comment fais-tu pour avoir cette humanité ? Et bien je leur réponds très simplement, je leur dit : C\'est ce goût de l\'amour, ce goût donc, qui m\'a poussé aujourd\'hui à entreprendre une construction mécanique, mais demain qui sait ? Peut-être simplement à me mettre au service de la communauté, à faire le don, le don de soi."

my_str = text
# Si on veut séparer suivant les mots et pas les phrases alors on rajoute le char : ' '
replacements = (',', '!', '?')
for r in replacements:
    my_str = my_str.replace(r, '.')

abc = my_str.split(".")

""" ATTENTION , ON FAIT L'HYPOTHESE QU'UNE PHRASE A MOINS DE 280 CHARACTERE !!!!!
    PS: ON FAIT l'hypothèse que un mot ne dépasse pas la limite de 280 char.
    """
limit = 280-4
k = 0
for i in range(0, len(abc)):
    if limit < len(abc[i]):
        k = i
        my_str = my_str.replace(' ', '.')
        break

abc = my_str.split(".")
for j in range(0, len(abc)):
    if limit < len(abc[j]):
        k = j
        break

length = 0
prevlength = 0
oldword = 0

tweets = []

while (oldword < len(abc)) and (limit > len(abc[k])):
    nbr_word = 0
    length = prevlength
    j = oldword
    while length-prevlength < limit and j < len(abc):
        length += len(abc[j])
        nbr_word += 1
        j += 1
    if length-prevlength > limit:
        length -= len(abc[j-1])
        nbr_word -= 1
    if text[prevlength] == ' ':
        #print(text[prevlength+1:length + nbr_word])
        #print()
        tweets = tweets + [text[prevlength+1:length + nbr_word]]
    else:
        #print(text[prevlength:length+nbr_word])
        #print()
        tweets = tweets + [text[prevlength:length+nbr_word]]
    prevlength = length+nbr_word
    oldword += nbr_word

if limit < len(abc[k]):
    print("ERROR : there are a word with more than 280 character")

if not len(tweets) == 1:
    for i in range(0, len(tweets)):
        tweets[i] = str(i+1) + '/' + str(len(tweets)) + ' ' + tweets[i]

for i in range(0, len(tweets)):
    print(tweets[i])



