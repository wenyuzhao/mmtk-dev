import re
# import env


def parse_log(file):
    record = False
    cm_rate = []
    with open(file) as f:
        for line in f:
            if "===== Chopin 23.11-chopin" in line and "PASSED" in line:
                break
            if "FinalMark start" in line:
                record = True
                continue
            if "finished." in line:
                record = False
                continue
            if not record:
                continue
            match = re.search(r"STW_CM_PACKETS_TIME=(\d+)ms .* STW_SCAN_NON_NULL_SLOTS=(\d+)", line)
            if match:
                cm_time = float(match.groups()[0])
                cm_objs = float(match.groups()[1])
                if cm_time > 0 and cm_objs > 0:
                    cm_rate.append((cm_time, cm_objs, cm_objs / cm_time))
    # print(cm_rate)
    for v in cm_rate:
        print(f"{v[2]:.1f}")


parse_log("x.log")
