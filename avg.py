sum = 0

f = open("results.txt", "r")
for i in range(5):
    sum += int(f.readline())
f.close()

f = open("results.txt", "a")
f.write("avg: "+str(sum/5))
f.close()