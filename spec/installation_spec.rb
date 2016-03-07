require 'serverspec'

do_iptables_tests = true

if ENV['TRAVIS']
    set :backend, :exec

    if ENV['FERM_MANAGEMENT'] != false
        do_iptables_tests = false
    end
end

describe 'redis Ansible role' do

    # Define variables
    packages = Array[]
    process_name = ''
    process_user = ''
    service_name = ''
    user_home = ''

    if ['debian', 'ubuntu'].include?(os[:family])
        packages = Array[ 'redis-server' ]
        process_name = 'redis-server'
        process_user = 'redis'
        service_name = 'redis-server'
        user_home = '/var/lib/redis'
    end

    # Begin tests
    it 'install role packages' do
        packages.each do |pkg_name|
            expect(package(pkg_name)).to be_installed
        end
    end

    describe user(process_user) do
        it { should exist }
        it { should belong_to_group process_user }
        it { should have_home_directory user_home }
        it { should have_login_shell '/bin/false' }
    end

    describe port('6379') do
        it { should be_listening }
    end

    describe process(process_name) do
        it { should be_running }
        its(:user) { should eq process_user }
    end

    describe service(service_name) do
        it { should be_enabled }
        it { should be_running }
    end

    if do_iptables_tests == true
        describe iptables() do
            it { should have_rule
                    '-A INPUT -p tcp -m tcp --dport 6379 -j ACCEPT' }
        end
    end
end

