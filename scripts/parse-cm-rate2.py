import re


def parse_log(file):
    record = False
    cm_time = None
    cm_objs = None
    cm_rate = []
    with open(file) as f:
        for line in f:
            if "===== DaCapo 23.11-chopin" in line and "PASSED" in line:
                break
            if "FinalMark start" in line:
                record = True
                continue
            if "finished." in line:
                record = False
                continue
            if not record:
                continue
            match = re.search(r"STW_CM_PACKETS_TIME=(\d+)ms", line)
            if match:
                cm_time = float(match.groups()[0])
            match = re.search(r"STW_SCAN_NON_NULL_SLOTS=(\d+)", line)
            if match:
                cm_objs = float(match.groups()[0])
                print(cm_objs, cm_time)
                assert cm_time is not None
                if cm_time != 0 and cm_objs != 0:
                    cm_rate.append((cm_time, cm_objs, cm_objs / cm_time))
                cm_time = None
    print(cm_rate)
    print("\n".join([f"{x[2]:.1f}" for x in cm_rate]))


parse_log("x.log")
