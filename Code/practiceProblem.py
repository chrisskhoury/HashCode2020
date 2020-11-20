from pprint import pprint
INPUT = r"d_tough_choices.txt"
OUTPUT = r"d.out"

libs = {}

with open(INPUT, "r") as reader:
    books_num, lib_num, days = reader.readline().strip("\n").split(" ")
    books_num, lib_num, days = int(books_num), int(lib_num), int(days)
    all_books = list(range(books_num))
    book_scores = list(reader.readline().strip("\n").split(" "))
    for i in range(lib_num):
        b, signup, speed = reader.readline().strip("\n").split(" ")
        b, signup, speed = int(b), int(signup), int(speed)
        books = list(map(int, list(reader.readline().strip("\n").split(" "))))
        libs[i] = [b, signup, speed, books]

books_map = {}
for i in all_books:
    books_map[i] = int(book_scores[i])

res = []

def getThroughput(lib_id):
    global days
    daysRemaining = days - libs[lib_id][1]
    x = libs[lib_id][2] * daysRemaining
    if x >= libs[lib_id][0]:
        return libs[lib_id][0], libs[lib_id][3]
    else:
        return x, libs[lib_id][3][:x]

def getScoreThroughput(lib_id):
    global days
    daysRemaining = days - libs[lib_id][1]
    if daysRemaining <= 0:
        return 0, []
    # total books that can ship in the remaining days
    x = libs[lib_id][2] * daysRemaining
    time_to_complete = x / libs[lib_id][2]
    if x >= libs[lib][0]:
        su = 0
        for i in libs[lib][3]:
            su += books_map[i]
        metric = (su / time_to_complete) * (daysRemaining / libs[lib_id][1])
        return metric, libs[lib][3]
    else:
        scores = {}
        for i in libs[lib][3]:
            scores[i] = books_map[i]
        sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}
        su = sum(list(sorted_scores.values())[:x])
        metric = (su / daysRemaining) * (daysRemaining / libs[lib_id][1])
        return metric, list(sorted_scores.keys())[:x]


def getMetric(lib_id):
    global days
    percentage = libs[lib_id][1] / days
    score = 0
    for i in libs[lib_id][3]:
        score += books_map[i]
    return score / percentage

while days >= 0:
    print(days)
    max_s = 0
    chosen_lib = None
    shipped_b = None
    for lib in libs:
        s, shipped = getScoreThroughput(lib)
        if s > max_s:
            max_s = s
            chosen_lib = lib
            shipped_b = shipped
    if max_s == 0:
        break

    res.append([chosen_lib, shipped_b])
    days -= libs[chosen_lib][1]
    del libs[chosen_lib]

    for s in shipped_b:
        all_books.remove(s)
        for lib in libs:
            try:
                libs[lib][3].remove(s)
            except Exception:
                pass

    keys = list(libs.keys()).copy()
    for k in keys:
        if len(libs[k][3]) == 0:
            del libs[k]

#print(all_books)
#pprint(libs)

with open(OUTPUT, "w") as writer:
    writer.write(str(len(res)) + '\n')
    for r in res:
        writer.write(str(r[0]) + ' ' + str(len(r[1])) + '\n')
        writer.write(' '.join(list(map(str,r[1]))) + '\n')
