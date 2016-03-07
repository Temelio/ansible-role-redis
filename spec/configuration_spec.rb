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
    process_user = ''
    server_config_file = ''

    if ['debian', 'ubuntu'].include?(os[:family])
        process_user = 'redis'
        server_config_file = '/etc/redis/redis.conf'
    end

    describe file(server_config_file) do
        it { should exist }
        it { should be_file }
        it { should be_owned_by 'redis' }
        it { should be_grouped_into 'redis' }
        it { should be_mode '600' }
    end

end

