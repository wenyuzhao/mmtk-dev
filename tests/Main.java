package tests;

public class Main {
    public static void main(final String[] args) {
        long x = 0;
        for (int i = 0; i < 10000000; i++) {
            writeFieldOnce(INSTANCE, i);
        }
        System.out.println("x=" + x + " " + INSTANCE.field + ' ' + INSTANCE.field[0]);
    }

    int[] field = new int[] { 0 };
    static Main INSTANCE = new Main();

    static void writeFieldOnce(Main x, int i) {
        // int[] arr = new int[] { i };
        // x.field = arr;
        // x.field = arr;
        Object[] arr = new Object[] { x };
        // System.out.println(i + " " + x.field);
        // return x;
    }
}