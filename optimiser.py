import subprocess


best = 18871

for cluster_size in range(1, 100):
    subprocess.check_output("python3 answer.py %d" % cluster_size, shell=True)

    command = "python3 validate.py answer.txt | tail -n 1 | awk '{print substr($3, 3)}'"
    output = subprocess.check_output(command, shell=True)
    try:
        curr_ans = float(output.decode("utf-8").rstrip())
        if curr_ans < best:
            print("New best %d for cluster %d" % (curr_ans, cluster_size))
            best = curr_ans
    except:
        pass

print(best)
