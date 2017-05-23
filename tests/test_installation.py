"""
Role installation tests
"""

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


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


def test_redis_server_service(host):
    """
    Check if database service is started and enabled
    """

    service = ''

    if host.system_info.distribution in ('debian', 'ubuntu'):
        service = 'redis-server'

    assert host.service(service).is_enabled

    # Systemctl not available with Docker images
    if host.backend.NAME != 'docker':
        assert host.service(service).is_running


def test_system_user(host):
    """
    Check if system user exists
    """

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
            '/etc/redis/redis.conf'
        ]

    for config_file in config_files:
        assert host.file(config_file).exists
        assert host.file(config_file).user == 'redis'
        assert host.file(config_file).group == 'redis'
        assert host.file(config_file).mode == 0o600


def test_redis_server_socket(host):
    """
    Check if Redis server listening
    """

    assert host.socket('tcp://127.0.0.1:6379').is_listening


def test_redis_server_process(host):
    """
    Check if Redis server process running
    """

    assert len(host.process.filter(user='redis', comm='redis-server')) == 1
