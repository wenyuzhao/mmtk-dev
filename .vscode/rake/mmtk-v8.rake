namespace "v8" do
    profile = ENV["profile"] || 'optdebug-mmtk'
    v8 = "./v8"
    mmtk = "./mmtk-v8/mmtk"
    octane = "~/octane"
    no_max_failures = true

    task :build do
        🔵 "cargo build", cwd:mmtk
        🔵 "MMTK_PLAN=#{$gc} ./tools/dev/gm.py x64.#{profile}.all", cwd:v8
    end

    task :test => :build do
        no_max_failures = no_max_failures ? "--exit-after-n-failures=0" : ""
        🔵 "MMTK_PLAN=#{$gc} ./tools/dev/gm.py x64.#{profile}.checkall #{no_max_failures}", cwd:v8
    end

    task :gdb do
        cmd = ARGV[(ARGV.index("--") + 1)..-1].join(" ")
        cmd.gsub! /x64\.(release|optdebug)/, 'x64.debug'
        profile = cmd.match(/x64\.(?<name>[\w\-_\d]+)/)[:name]
        Rake::Task["v8:build"].invoke
        🔵 "gdb -ex='set confirm on' -ex r -ex q --args #{cmd}", cwd:v8
        exit 0
    end

    task :octane => :build do
        cwd = ENV['PWD']
        🔵 "#{cwd}/v8/out/x64.#{profile}/d8 ./run.js", cwd:octane
    end
end

