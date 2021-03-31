include ../../common.mk

all: librust_mmtk_probe.so librust_mmtk_probe_32.so

librust_mmtk_probe.so: rust_mmtk_probe.o
	gcc $(CFLAGS) -pthread -shared -o librust_mmtk_probe.so rust_mmtk_probe.o -lc

rust_mmtk_probe.o: rust_mmtk_probe.c
	gcc $(CFLAGS) -pthread -c rust_mmtk_probe.c -I$(JDK)/include -I$(JDK)/include/linux/

librust_mmtk_probe_32.so: rust_mmtk_probe_32.o
	gcc $(CFLAGS) -m32 -pthread -shared -o librust_mmtk_probe_32.so rust_mmtk_probe_32.o -lc

rust_mmtk_probe_32.o: rust_mmtk_probe.c
	gcc $(CFLAGS) -m32 -pthread -c rust_mmtk_probe.c -o rust_mmtk_probe_32.o -I$(JDK)/include -I$(JDK)/include/linux/

clean:
	rm -rf *.o *.so

test: default
	$(JAVA) -Djava.library.path=`pwd`/rust_mmtk_probe -cp .:$(BENCHMARKS)/dacapo/dacapo-9.12-bach.jar Harness -c callback.DacapoBachCallback avrora
