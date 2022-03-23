
namespace "bench" do
    config = ENV['config']
    moma = ENV['moma']
    dest = -> { "#{moma}.moma:/home/wenyuz/" }

    def rsync(src, dst)
        🔵 "rsync -azR --no-i-r -h --info=progress2 #{src} #{dst}"
    end

    task :rsync do
        rsync("~/./MMTk-Dev/evaluation/running-ng", dest.())
        rsync("~/./MMTk-Dev/evaluation/configs/#{config}", dest.())
        rsync("~/./MMTk-Dev/evaluation/configs/*.yml", dest.())
        rsync("~/./MMTk-Dev/evaluation/configs/*.sh", dest.())
        rsync("~/./MMTk-Dev/evaluation/advice", dest.())
        rsync("~/./MMTk-Dev/evaluation/probes", dest.())
        puts "❗️ Please run `pip3 install -e . --user` on #{moma}.moma and add `~/.local/bin` to PATH."
    end

    task :cp do
        name = ENV['name']
        🔵 "cp -r ./mmtk-openjdk/repos/openjdk/build/linux-x86_64-normal-server-release ~/MMTk-Dev/evaluation/configs/#{name}"
    end
end