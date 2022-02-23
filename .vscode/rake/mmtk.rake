ENV["RUST_BACKTRACE"] = "1"

if ENV.has_key?("threads")
    ENV['MMTK_THREADS'] = ENV["threads"]
end

$gc = ENV['gc'] || 'NoGC'

if $gc == $gc.downcase
    ENV['MMTK_PLAN'] = $gc
end

namespace "mmtk" do
    task :ci_style do
        🔵 "bash ./.github/scripts/ci-style.sh", cwd: './mmtk-core'
    end

    task :ci_test do
        🔵 "bash ./.github/scripts/ci-test.sh", cwd: './mmtk-core'
    end

    task :ci_doc do
        🔵 "bash ./.github/scripts/ci-doc.sh", cwd: './mmtk-core'
    end

    task :ci => [:ci_style, :ci_test]
end
