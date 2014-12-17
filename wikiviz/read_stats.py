
def do_average(output_filename):
    file2 = open("avg_stats1.csv","w")
    file1 = open("out4.csv", 'r')

    lines = file1.readlines()
    stats = {}
    greedy_sum = 0
    for count,i in enumerate(lines[:]):
        if len(i.split(","))==3:
            file2.writelines(i)
            continue
        else:
            continue
        if 'gen' in i or "Ant" in i:
            continue

    

        i = i.split("\t")
        if "GREEDY" ==i[0]:
            greedy_sum += float(i[1])
            continue
        try:
            generation_sums, counter = stats[i[0]]
            for j in range(0,len(generation_sums)):
                generation_sums[j] += float(i[j+1])
            stats[i[0]][1] +=1
        except:
            stats[i[0]] = [[float(field) for field in i[1:]],1]

    file1.close()

    output = open(output_filename,"w")
    for i in sorted(stats.keys(), key= lambda x : int(x)):
        gen_list, total_g = stats[str(i)]
        o_string = str(i)

        for j in gen_list:
            o_string+= ","+str(j/float(total_g))
        output.writelines(o_string[:-1]+"\n")
    output.writelines("\nGreedy,"+str(greedy_sum/10.0)+"\n")
    output.close()

if __name__=='__main__':
    do_average("output_file.txt")