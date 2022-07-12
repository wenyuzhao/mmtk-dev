namespace "jdk" do
    # Args
    profile = ENV["profile"] || 'fastdebug'
    heap = ENV["heap"] || '100M'
    n = ENV["n"] || '1'
    benchmark = ENV["bench"] || 'xalan'
    interpreter_only = ENV.has_key?("int")
    disable_c1 = ENV.has_key?("noc1")
    disable_tlab_zeroing = ENV.has_key?("nozero")
    fixed_mutator_threads = ENV.has_key?("t")
    if ENV.has_key?("features")
        ENV["GC_FEATURES"] = ENV["features"]
    end

    # Other configs
    vm_args = "-XX:MetaspaceSize=1G -XX:-UseBiasedLocking"
    heap_args = -> { "-Xms#{heap} -Xmx#{heap}" }
    mmtk_args = "-XX:+UseThirdPartyHeap -Dprobes=RustMMTk"
    if interpreter_only
        vm_args += ' -Xint'
    end
    if disable_c1
        vm_args += ' -XX:-TieredCompilation' # -Xcomp
    end
    if disable_tlab_zeroing
        vm_args += ' -XX:+ZeroTLAB -XX:-ReduceFieldZeroing -XX:-ReduceBulkZeroing'
    end
    bm_args = "#{$dacapo_args.($dacapo_new_jar)} -n #{n} -c probe.DacapoChopinCallback #{benchmark}"
    jdk = "./openjdk"
    mmtk = "./mmtk-openjdk/mmtk"
    conf = -> { "linux-x86_64-normal-server-#{profile}" }
    java = -> { "#{jdk}/build/#{conf.()}/jdk/bin/java" }
    if fixed_mutator_threads
        bm_args += ' -t ' + ENV["t"]
    end

    task :config do
        🔵 "sh configure --disable-warnings-as-errors --with-debug-level=#{profile} --with-target-bits=64 --with-native-debug-symbols=zipped --with-jvm-features=shenandoahgc", cwd:jdk
    end

    task :build do
        🔵 "make --no-print-directory CONF=#{conf.()} THIRD_PARTY_HEAP=$PWD/../mmtk-openjdk/openjdk", cwd:jdk
    end

    task :clean do
        🔵 "make --no-print-directory CONF=#{conf.()} clean", cwd:jdk
    end

    task :fix_mmtk do
        🔵 "cargo clean", cwd:mmtk
    end

    task :test => :build do
        🔵 "MMTK_PLAN=#{$gc} #{java.()} #{vm_args} #{heap_args.()} #{mmtk_args} #{bm_args}"
    end

    task :gdb => :build do
        🔵 "MMTK_PLAN=#{$gc} gdb --args #{java.()} #{vm_args} #{heap_args.()} #{mmtk_args} #{bm_args}"
    end

    namespace "hs" do
        mn = ENV["mn"] || '33M'
        openjdk_gc_args = " -XX:+UnlockExperimentalVMOptions -XX:-UseCompressedOops -XX:-UseCompressedClassPointers -XX:G1HeapRegionSize=1M -XX:TLABSize=32K -XX:-ResizeTLAB -XX:SurvivorRatio=32 -XX:-UseAdaptiveSizePolicy -Xmn#{mn} -XX:+Use#{$gc}GC"
        # openjdk_gc_args = " -XX:+UnlockExperimentalVMOptions -XX:-UseCompressedOops -XX:-UseCompressedClassPointers -XX:+Use#{$gc}GC"
        hs_args = ENV["hs_args"] || ''

        task :test => :build do
            🔵 "#{$jvmti_env} #{java.()} #{vm_args} #{heap_args.()} #{openjdk_gc_args} #{$jvmti_args} #{hs_args} #{bm_args}"
        end
    end
end