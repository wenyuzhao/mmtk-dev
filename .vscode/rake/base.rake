# Rakefile
$command_finished = true
at_exit { $command_finished || sleep(1) }

def 🔵(command, cwd: '.')
    puts "🔵 #{command}"
    $command_finished = false
    res = system("cd #{cwd} && #{command}")
    $command_finished = true
    res || raise('❌')
end

task :hello do
    🔵 "echo Hello!"
end

task :init do
    🔵 "pip3 install -e . --user", cwd: '$PWD/evaluation/running-ng'
    🔵 "make native-code", cwd: '$PWD/evaluation/probes'
    puts "❗️ Please add `~/.local/bin` to PATH."
end