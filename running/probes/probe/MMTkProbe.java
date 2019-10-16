package probe;

import java.lang.reflect.*;

public class MMTkProbe implements Probe {
  private Method beginMethod;
  private Method endMethod;

  public void init() {
    try {
      Class harnessClass = Class.forName("org.jikesrvm.mm.mminterface.MemoryManager");
      beginMethod = harnessClass.getMethod("harnessBegin");
      endMethod = harnessClass.getMethod("harnessEnd");
    } catch (Exception e) {
      throw new RuntimeException("Unable to find JikesRVM MemoryManager.harnessBegin and/or MemoryManager.harnessEnd", e);
    }
  }

  public void cleanup() {
    // Nothing to do
  }

  public void begin(String benchmark, int iteration, boolean warmup) {
    if (warmup) return;
    try {
      beginMethod.invoke(null);
    } catch (Exception e) {
      throw new RuntimeException("Error running MemoryManager.harnessBegin", e);
    }
  }

  public void end(String benchmark, int iteration, boolean warmup) {
    if (warmup) return;
    try {
      endMethod.invoke(null);
    } catch (Exception e) {
      throw new RuntimeException("Error running MemoryManager.harnessBegin", e);
    }
  }

  public void report(String benchmark, int iteration, boolean warmup) {
    // Done within end.
  }
}

