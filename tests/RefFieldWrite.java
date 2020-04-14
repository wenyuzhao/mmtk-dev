package tests;

public class RefFieldWrite {
    int[] field = new int[] { 0 };
    static RefFieldWrite INSTANCE = new RefFieldWrite();

    static void writeFieldOnce(RefFieldWrite x, int i) {
        x.field = new int[] { i };
        System.out.println(i + " " + x.field);
    }

    public static void main(String[] args) {
        for (int i = 0; i < 500; i++) {
            writeFieldOnce(INSTANCE, i);
        }
    }
}