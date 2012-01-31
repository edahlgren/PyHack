"""
Module :: Hacker News Dissection

Creator :: Erin Dahlgren

Date :: January 30 2012

      The purpose of the module is to compare Hacker news to English.
      The result is an idea of how 'hackish' hacker news is! So great!
      Hope you enjoy it.

"""



from BeautifulSoup import BeautifulSoup
import re
import operator
import sys
import string
import urllib2

base = "http://news.ycombinator.com"

# standard stopwords used in text mining
stopwords = ["a","able","about","across","after","all","almost","also","am","among","an","and","any","are","as","at","be","because","been","but","by","can","cannot","could","dear","did","do","does","either","else","ever","every","for","from","get","got","had","has","have","he","her","hers","him","his","how","however","i","if","in","into","is","it","its","just","least","let","like","likely","may","me","might","most","must","my","neither","no","nor","not","of","off","often","on","only","or","other","our","own","rather","said","say","says","she","should","since","so","some","than","that","the","their","them","then","there","these","they","this","tis","to","too","twas","us","wants","was","we","were","what","when","where","which","while","who","whom","why","will","with","would","yet","you","your$"]

# I'm fixing the data to fifteen pages worth of posts, thus 30*15 = 450 titles and rankings
# because this scrapes the data live.  I wanted realtime stats.
# But I don't want my code to cause anyone's server to go down

# First question: 
# What are the most popular words, disregarding post popularity?
# 
# Second question:
# What words are in the most popular posts?
#
# Third question:
# How unenglish is hacker news? In other words, how hackish? !!
#


def readme(path):
    return open(path).read()

def getpage(suffix):
    page = urllib2.urlopen(base + suffix)
    soup = BeautifulSoup(page)
    return soup.findAll("tr", style=None)


def nopunct(stringy):
    nopuncts = stringy.translate(None, string.punctuation)
    return nopuncts


def getinfo(trs):
    imatrix = []
    for i in range(3, 62, 2):
        title = nopunct(str(trs[i].contents[0].nextSibling.nextSibling.contents[0].contents[0]).lower())
        try:
            pstr = str(trs[i+1].contents[0].nextSibling.contents[0].contents[0])
            points = int(pstr.split(" ")[0])
        except:
            pass
        imatrix.append([points, title])
    return imatrix


def getnext(trs):
    tag = str(trs[63].contents[0].nextSibling.contents[0]).split(" ")[1]
    return str(tag[6:len(tag)-1])


def recurse_through(suffix, corpus, i):
    if i < 15:
        print "Processing page ", i+1
        p = getpage(suffix)
        corpus_i = corpus + getinfo(p)
        suffix_i = getnext(p)
        return recurse_through(suffix_i, corpus_i, (i+1))
    else:
        return corpus


# Data! 
v = recurse_through("/newest", [], 0)

def spacify(num):
    if num == 0:
        return 0
    else:
        print " "
        return spacify(num-1)

def reask(prompter, data):
    print "Ask another question?  press enter to go back to prompt"
    back = sys.stdin.readline()
    if back == "\n":
        prompter(data)
    else: return 0

def prompt(data):
    spacify(4)
    print "Hacker News Dissection!  Ha Ha!"
    spacify(2)
    print "What are the most popular words, disregarding post popularity?"
    print "\t type 1"
    spacify(1)
    print "What words are in the most popular posts?"
    print "\t type 2"
    spacify(1)
    print "How much of a language hack is hacker news?"
    print "\t type 3"
    spacify(1)
    print "type exit, to quit"
    ask = sys.stdin.readline()
    if ask == "1\n":
        spacify(12)
        print "Computing top 20 most titled words."
        spacify(1)
        print "word", "\t\t\t", "times in a title"
        print "----", "\t\t\t", "----------------"
        quest_onetwo(data, "one")
        print "----------------------------------"
        reask(prompt, data)
    if ask == "2\n":
        spacify(12)
        print "Computing top 20 most well-read words."
        spacify(1)
        print "word", "\t\t\t", "net points from title's points"
        print "----", "\t\t\t", "----------------"
        quest_onetwo(data, "title")
        print "----------------------------------"
        reask(prompt, data)
    if ask == "3\n":
        spacify(12)
        print "Computing English versus Hacker News!"
        spacify(1)
        quest_three(data)
        print "----------------------------------"
        reask(prompt, data)
    if ask == "exit\n":
        return 0


def top20(questdict):
    questlist = [(val, key) for key, val in questdict.items()]
    questlist.sort(reverse=True)
    for i in range(0,21):
        if questlist[i][1] != '':
            print questlist[i][1], "\t\t\t", questlist[i][0] 


def quest_onetwo(data, param):
    qdict = {}
    dontwantum = r'$|^'.join(["^i","my","me"]+stopwords)
    for title in data:
        words = title[1].split(" ")
        for w in words:
            if (not re.search(dontwantum, w)):
                if param == "title":    
                    try:
                        qdict[w] += title[0]
                    except:
                        qdict[w] = title[0]
                else:
                    try:
                        qdict[w] += 1
                    except:
                        qdict[w] = 1
    top20(qdict)


def displayhack(w,i):
    print "out of", w, "hacker news words,", i, "are total hacks!"
    print " "
    print "Here are some examples of the most hackerish"
    print "--------------------------------------------"
    print "hack", "\t\t\t", "times"
    print " "


def quest_three(data):
    hackerish_i = 0
    hackerish_w = 0
    hackerish = {}
    english = nopunct(readme("./american-english")).split("\n")
    for title in data:
        words = title[1].split(" ")
        for w in words:
            hackerish_w += 1
            if not(w in english) and not(re.search(r"[0-9]", w)):
                hackerish_i += 1
                try:
                    hackerish[w] += 1
                except:
                    hackerish[w] = 1
    displayhack(hackerish_w, hackerish_i)
    top20(hackerish)

   
# running for the user!
def main():
    prompt(v)

if __name__ == "__main__":
    main()


