namespace "jks" do
    profile = ENV["profile"] || 'RBaseBaseSemiSpace'
    heap = ENV["heap"] || '100M'
    benchmark = ENV["bench"] || 'xalan'
    n = ENV["n"] || '1'

    jks = "./jikesrvm"
    build_args = "--m32 --answer-yes --use-third-party-heap=../mmtk-jikesrvm --use-third-party-build-configs=../mmtk-jikesrvm/jikesrvm/build/configs/ --use-external-source=../mmtk-jikesrvm/jikesrvm/rvm/src"
    if ENV.has_key?("q") || ENV.has_key?("quick")
        build_args += " -q"
    end
    rvm = -> { "#{jks}/dist/#{profile}_x86_64_m32-linux/rvm" }
    heap_args = -> { "-Xms#{heap} -Xmx#{heap}" }
    bm_args = "#{$dacapo_args.($dacapo_9_12_jar)} -n #{n} -c probe.DacapoBachCallback #{benchmark}"

    task :build do
        🔵 "./bin/buildit localhost #{profile} #{build_args}", cwd:jks
    end

    task :test do
        🔵 "#{rvm.()} #{heap_args.()} #{bm_args}"
    end
end