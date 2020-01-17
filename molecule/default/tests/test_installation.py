"""
Role tests
"""

import os
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_packages(host):
    """
    Check if packages are installed
    """

    packages = []

    if host.system_info.distribution in ('debian', 'ubuntu'):
        packages = [
            'redis-server',
            'redis-sentinel',
        ]

    for package in packages:
        assert host.package(package).is_installed


def test_redis_services(host):
    """
    Check if database and sentinel services are started and enabled
    """

    services = []

    if host.system_info.distribution in ('debian', 'ubuntu'):
        services = ['redis-server', 'redis-sentinel']

    for service in services:
        assert host.service(service).is_enabled

        assert host.service(service).is_running


def test_system_user(host):
    """
    Check if system user exists
    """
    if host.system_info.codename == 'bionic':
        assert host.user('redis').exists
        assert host.user('redis').group == 'redis'
        assert host.user('redis').home == '/var/lib/redis'
        assert host.user('redis').shell == '/usr/sbin/nologin'
    elif host.system_info.codename == 'disco':
        assert host.user('redis').exists
        assert host.user('redis').group == 'redis'
        assert host.user('redis').home == '/var/lib/redis'
        assert host.user('redis').shell == '/usr/sbin/nologin'
    else:
        assert host.user('redis').exists
        assert host.user('redis').group == 'redis'
        assert host.user('redis').home == '/var/lib/redis'
        assert host.user('redis').shell == '/bin/false'


def test_config_files(host):
    """
    Check if configuration files exists
    """

    config_files = []

    if host.system_info.distribution in ('debian', 'ubuntu'):
        config_files = [
            '/etc/redis/redis.conf',
            '/etc/redis/sentinel.conf',
        ]

    for config_file in config_files:
        assert host.file(config_file).exists
        assert host.file(config_file).user == 'redis'
        assert host.file(config_file).group == 'redis'
        assert host.file(config_file).mode == 0o600


def test_redis_sockets(host):
    """
    Check if Redis server and Sentinel are listening
    """

    # Redis server
    assert host.socket('tcp://127.0.0.1:6379').is_listening

    # Redis Sentinel
    assert host.socket('tcp://127.0.0.1:26379').is_listening


def test_redis_processes(host):
    """
    Check if Redis server and Sentinel processes are running
    """

    # Redis server
    assert len(host.process.filter(user='redis', comm='redis-server')) == 1

    # Redis Sentinel
    assert len(host.process.filter(user='redis', comm='redis-sentinel')) == 1


def test_warnings_in_log_files(host):
    """
    Check we have no warning in logs, with the optmization tasks enabled and
    sysfs rules
    """

    log_files_paths = [
        '/var/log/redis/redis-server.log',
        '/var/log/redis/redis-sentinel.log',
    ]

    for log_file_path in log_files_paths:
        run_command = 'grep -i "warning" {}'.format(log_file_path)
        assert host.run_expect([1], run_command)
