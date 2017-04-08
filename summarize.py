import os


def summary():
    file1 = "data/summary_cluster.txt"
    file2="data/summary_classfication.txt"
    summary_file = "data/summary.txt"
    try:
        os.remove(summary_file)
    except OSError:
        pass

    f2 = open(file1, 'r')
    data1=f2.read()
    f1 = open(summary_file, "a")
    file = open(file2, 'r')
    data2=file.read()
    
    print(data1 + data2)
    f1.write(data1+data2)

    f1.close()




if __name__ == '__main__':
    summary()