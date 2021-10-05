public class TotalAllocation {
    private static int enabled = 0;

    private static native void alloc(Object o);

    // Instrument two allocation bytecodes
    // new is a Java keyword
    public static void new_(Object o) {
        if (enabled != 0) {
            alloc(o);
        }
    }

    public static void newarray(Object a) {
        if (enabled != 0) {
            alloc(a);
        }
    }
}
