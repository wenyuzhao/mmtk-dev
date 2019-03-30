
def parseFile(file):
    with open(file) as f:
        startRecording = False
        result = []
        for line in f:
            line = line.strip()
            if line == '===== LatencyTimer Pause Times =====':
                startRecording = True
            elif line == '===== LatencyTimer Pause Times End =====':
                startRecording = False
            elif startRecording and line.isdigit():
                try:
                    result.append(int(line))
                except:
                    pass
        return result

print(parseFile('../pause-time-results/results/lusearch.1416.113.FastAdaptiveRegional.s.wr.lt.log'))

