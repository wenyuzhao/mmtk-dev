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
    🔵 "make native-code", cwd: '$PWD/evaluation/probes'
end