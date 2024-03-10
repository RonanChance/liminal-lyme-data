
import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

mystr = "Whats going on everyone.\n\nSo, from the title, I am starting this combo of drugs to attempt to help my long term GAD, panic disorder, derealization and agoraphobia. For some background info before people start saying don't go on benzos... I was on Klonopin for three years for intense insomnia due to undiagnosed Lyme disease and completely know the consequences of long term use. Benzos, however, were the only drugs that ever worked for my anxiety. Before this post I was prescribed 5 pills of Xanax, 1mg, a month for extreme panic attacks, however, this only proved to be a crutch and nothing more.\n\nTo extend on my previous statements about benzodiazepines, I have tried everything beyond this terribly perfect medication to help solve my problems. I have undergone the most extensive blood work money can buy and spent 3 months at a Lyme and cancer center in Ariziona treating all issues such as lyme, mold, co-infections etc (if you would like to hear what treatments I went through please dm me). I purchased a hyperbaric chamber for my home, did NAD+ treatments on a strict schedule (4 first week, 3 second, 2.. etc.). Went gluten, dairy, sugar, caffeine, and alcohol free while being monitored by a nutritionist for my supplement intake. Personal trainer 5 days a week. Sauna and steam rooms daily. EDMR, CBT, DBT and hypnosis 2x a week. Attempted ketamine for 6 sessions for depression but made the derealization worse.\n\nI have attempted everything that was available to me and I am now going with this course of action in order to live a normal life for my last year of college. I am not looking for advice, however, constructive, helpful points would be appreciated. Please ask me anything.\n\nNonetheless, I will be documenting my progress on these medications, (side effects, benefits, etc) for the next two months. Please ask me anything or any advice you would like\n\nRound 5 - Lamictal, Zoloft, Propranolol, Klonopin. My new set of drugs, follow my progress."
mystr2 = "Is there a connection between mitochondrial dysfunction and Lyme and/or the antibiotics we get put on. It\u2019s hard to fathom how much less energy output I have after treatment. I have a hard time believing it is just Lyme. I\u2019ve been taking a lot of supplement for mitochondrial health like NAD+, magnesium, and coq10. Seeing slight improvements but not a lot."

filtered_words_list = [word for word in mystr2
                      .replace(" im "," ")
                      .replace("."," ")
                      .replace("!"," ")
                      .replace(",", " ")
                      .replace("?"," ")
                      .replace("("," ")
                      .replace(")", " ")
                      .replace("’", "")
                      .replace("&amp;#x200b;", " ")
                      .replace("\"", " ")
                      .replace("/", " ")
                      .replace("\'", " ")
                      .replace("=", " ")
                      .replace("*", "")
                      .split() if word.lower() not in stop_words]
    
filtered_words = " ".join(filtered_words_list)

word = "NAD+".lower() + " "
# make sure our term is in the filtered data, and NONE of the terms to avoid are there
# print(filtered_words)
# if (word in filtered_words):
#     print(word)
