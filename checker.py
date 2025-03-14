import os
from difflib import SequenceMatcher
from os import listdir
from os.path import isfile, join

## ration = 2M/T
## M - numarul de caractere care se potrivesc exact
# T - suma lungimilor celor 2 text
# Gestalt pattern matching algorithm
# Ideea : Comparam doua secvente in paralel si o gasim pe cea mai lunga subsecv comuna si apelam recursiv pe celelalte ramase - algoritmul este deja implementat in difflib !


def similarity_html(file1, file2):
    file1 = os.path.expanduser(file1)
    file2 = os.path.expanduser(file2)

    with open(file1, "r", encoding="utf-8") as f1, open(file2, "r", encoding="utf-8") as f2:
        content1 = f1.read()
        content2 = f2.read()

    return SequenceMatcher(None, content1, content2).ratio()

# score = similarity_html("~/Desktop/Veridion/tier1/aemails.org.html",
#                         "~/Desktop/Veridion/tier1/akashinime.guru.html")

# print(f"Similarity score: {score:.2%}")




def add_from_tier(file3):
    onlyfiles = [f for f in listdir(file3) if isfile(join(file3, f))]
    return onlyfiles

file3 = "tier1"
onlyfiles = add_from_tier(file3)



final_list = [];
def check_all(onlyfiles):
    remaining_files = onlyfiles[:]
    final_list = []
    while remaining_files:
        i = remaining_files.pop(0)
        group = [i]
        for m in remaining_files[:]:
            score = similarity_html(f"tier1/{i}", f"tier1/{m}")
            if score >= 0.70:
                group.append(m)
                remaining_files.remove(m)
        final_list.append(group)
    return final_list


final_list = check_all(onlyfiles)
print(final_list)
