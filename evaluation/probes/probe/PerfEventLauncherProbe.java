package probe;


//PERF_EVENT_NAMES is set to EVENT1,fd0,fd1,...fdn;EVENT2,fd0,fd1,....
//TODO: create testing for the new feature.
public class PerfEventLauncherProbe implements Probe {

  private static String[] eventNames;
  private static int[][] eventFds;
  
  private static native void enable(int fd);
  private static native void disable(int fd);
  private static native void reset(int fd);
  private static native void read(int fd, long[] result);

  private final long[] results = new long[3];
  private long[][] initialCounters;
  private long[][] endCounters;
  
  static {
    System.loadLibrary("perf_event_launcher");
  }

  
  public void init()
  {
    System.out.println("PERF_EVENT_NAMES is " + System.getenv("PERF_EVENT_NAMES"));
      
    String[] events = System.getenv("PERF_EVENT_NAMES").split(";");
    eventNames = new String[events.length];
    eventFds = new int[events.length][];
    initialCounters = new long[events.length][];
    endCounters = new long[events.length][];
    for (int i=0; i< events.length; i++){
      String[] str = events[i].split(",");
      eventNames[i] = str[0];
      eventFds[i] = new int[str.length-1];
      initialCounters[i] = new long[str.length-1];
      endCounters[i] = new long[str.length-1];
      for (int j=1;j<str.length;j++)
	eventFds[i][j-1] = Integer.decode(str[j]).intValue();	
    }
  }

  public void cleanup(){
    System.out.println("cleanup is called");
  }

  public void begin(String benchmark, int iteration, boolean warmup){
    System.out.println("begin is called at iteration " + iteration);
    
    for(int i=0; i< eventNames.length; i++){
      for(int j=0; j<eventFds[i].length; j++){
        read(eventFds[i][j], results);
        initialCounters[i][j] = results[0];
        enable(eventFds[i][j]);
      }
    }
    
  }

  public void end(String benchmark, int iteration, boolean warmup){
    System.out.println("end is called at iteration " + iteration);
    
    for(int i=0; i< eventNames.length; i++){
      for(int j=0; j<eventFds[i].length; j++){
        disable(eventFds[i][j]);
        read(eventFds[i][j], results);
        endCounters[i][j] = results[0];
      }
    }
    
  }

  public void report(String benchmark, int iteration, boolean warmup){
    System.out.println("report is called at iteration " + iteration);

    if (warmup) {
      System.out.println("============================ Perf Counter warmup " + iteration + " ============================");
    }
    else {
      System.out.println("============================ Perf Counter ============================");
    }
    
    for(int i=0; i< eventNames.length; i++)
      for(int j=0; j<eventFds[i].length; j++) {
        String cpu = ":CPU"; 
        if (eventFds[i].length == 1) {
          cpu = cpu + "(all)";
        }
        else {
          cpu = cpu + j;
        }
        System.out.println(eventNames[i] + cpu + ":" + (endCounters[i][j]-initialCounters[i][j]));
      }

    System.out.println("");

    System.out.println("------------------------------ Perf Counter Statistics -----------------------------");
  }

}

