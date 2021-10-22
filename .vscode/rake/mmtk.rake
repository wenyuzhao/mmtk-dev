ENV["RUST_BACKTRACE"] = "1"

if ENV.has_key?("threads")
    ENV['MMTK_THREADS'] = ENV["threads"]
end

$gc = ENV['gc'] || 'NoGC'

if $gc == $gc.downcase
    ENV['MMTK_PLAN'] = $gc
end