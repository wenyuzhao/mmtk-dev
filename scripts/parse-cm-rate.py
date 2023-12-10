import re


def parse_log(file):
    record = False
    cm_time = None
    cm_objs = None
    cm_rate = []
    with open(file) as f:
        for line in f:
            if "Early terminate SATB:" in line:
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
            match = re.search(r"STW_SCAN_OBJS=(\d+)", line)
            if match:
                cm_objs = float(match.groups()[0])
                assert cm_time is not None
                cm_rate.append((cm_time, cm_objs, cm_objs / cm_time))
    print(cm_rate)


parse_log("x.log")
