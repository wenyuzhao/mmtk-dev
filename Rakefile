# Rakefile
task default: [:hello]

$command_finished = true
at_exit { $command_finished || sleep(1) }

def 🔵(command, cwd: '.')
    puts "🔵 #{command}"
    $command_finished = false
    res = system("cd #{cwd} && #{command}")
    $command_finished = true
    res || raise('❌')
end

ENV["RUSTUP_TOOLCHAIN"] = "nightly-2021-05-12"
ENV["RUST_BACKTRACE"] = "1"
ENV['MMTK_PLAN'] = ENV['gc'] || 'NoGC'
if ENV.has_key?("threads")
    ENV['MMTK_THREADS'] = ENV["threads"]
end

namespace "v8" do
    profile = ENV["profile"] || 'optdebug-mmtk'
    v8 = "./v8"
    mmtk = "./mmtk-v8/mmtk"
    no_max_failures = true

    task :build do
        🔵 "cargo build", cwd:mmtk
        🔵 "./tools/dev/gm.py x64.#{profile}.all", cwd:v8
    end

    task :test => :build do
        no_max_failures = no_max_failures ? "--exit-after-n-failures=0" : ""
        🔵 "./tools/dev/gm.py x64.#{profile}.checkall #{no_max_failures}", cwd:v8
    end

    task :gdb do
        cmd = ARGV[(ARGV.index("--") + 1)..-1].join(" ")
        cmd.gsub! /x64\.(release|optdebug)/, 'x64.debug'
        profile = cmd.match(/x64\.(?<name>[\w\-_\d]+)/)[:name]
        Rake::Task["v8:build"].invoke
        🔵 "gdb -ex='set confirm on' -ex r -ex q --args #{cmd}", cwd:v8
        exit 0
    end
end

namespace "jdk" do
    profile = ENV["profile"] || 'fastdebug'
    heap = ENV["heap"] || '100M'
    benchmark = ENV["bench"] || 'xalan'
    n = ENV["n"] || '1'

    vm_args = "-XX:MetaspaceSize=1G"
    heap_args = -> { "-Xms#{heap} -Xmx#{heap}" }
    mmtk_args = "-XX:+UseThirdPartyHeap -Dprobes=RustMMTk"
    if ENV.has_key?("int")
        mmtk_args += ' -Xint'
    end
    if ENV.has_key?("noc1")
        mmtk_args += ' -XX:-TieredCompilation  -Xcomp'
    end
    if ENV.has_key?("nozero")
        mmtk_args += ' -XX:+ZeroTLAB -XX:-ReduceFieldZeroing -XX:-ReduceBulkZeroing'
    end
    probes = "$PWD/evaluation/probes"
    dacapo_9_12 = "-Djava.library.path=#{probes} -cp #{probes}:#{probes}/probes.jar:/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar Harness"
    bm_args = "#{dacapo_9_12} -n #{n} -c probe.DacapoBachCallback #{benchmark}"
    jdk = "./mmtk-openjdk/repos/openjdk"
    mmtk = "./mmtk-openjdk/mmtk"
    conf = -> { "linux-x86_64-normal-server-#{profile}" }
    java = -> { "#{jdk}/build/#{conf.()}/jdk/bin/java" }

    task :config do
        🔵 "sh configure --disable-warnings-as-errors --with-debug-level=#{profile} --with-target-bits=64 --disable-zip-debug-info", cwd:jdk
    end

    task :build do
        🔵 "make --no-print-directory CONF=#{conf.()} THIRD_PARTY_HEAP=$PWD/../../openjdk", cwd:jdk
    end

    task :test => :build do
        🔵 "#{java.()} #{vm_args} #{heap_args.()} #{mmtk_args} #{bm_args}"
    end

    task :gdb => :build do
        🔵 "gdb --args #{java.()} #{vm_args} #{heap_args.()} #{mmtk_args} #{bm_args}"
    end
end


namespace "jks" do
    profile = ENV["profile"] || 'RBaseBaseSemiSpace'
    heap = ENV["heap"] || '100M'
    benchmark = ENV["bench"] || 'xalan'
    n = ENV["n"] || '1'

    jks = "./mmtk-jikesrvm/repos/jikesrvm"
    build_args = "--m32 --answer-yes --use-third-party-heap=../../ --use-third-party-build-configs=../../jikesrvm/build/configs/ --use-external-source=../../jikesrvm/rvm/src"
    if ENV.has_key?("q") || ENV.has_key?("quick")
        build_args += " -q"
    end
    rvm = -> { "#{jks}/dist/#{profile}_x86_64_m32-linux/rvm" }
    heap_args = -> { "-Xms#{heap} -Xmx#{heap}" }
    probes = "$PWD/evaluation/probes"
    dacapo_9_12 = "-Djava.library.path=#{probes} -cp #{probes}:#{probes}/probes.jar:/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar Harness"
    bm_args = "#{dacapo_9_12} -n #{n} -c probe.DacapoBachCallback #{benchmark}"

    task :build do
        🔵 "./bin/buildit localhost #{profile} #{build_args}", cwd:jks
    end

    task :test do
        🔵 "#{rvm.()} #{heap_args.()} #{bm_args}"
    end
end