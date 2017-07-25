# redis

[![Build Status](https://img.shields.io/travis/infOpen/ansible-role-redis/master.svg?label=travis_master)](https://travis-ci.org/infOpen/ansible-role-redis)
[![Build Status](https://img.shields.io/travis/infOpen/ansible-role-redis/develop.svg?label=travis_develop)](https://travis-ci.org/infOpen/ansible-role-redis)
[![Updates](https://pyup.io/repos/github/infOpen/ansible-role-redis/shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-redis/)
[![Python 3](https://pyup.io/repos/github/infOpen/ansible-role-redis/python-3-shield.svg)](https://pyup.io/repos/github/infOpen/ansible-role-redis/)
[![Ansible Role](https://img.shields.io/ansible/role/8368.svg)](https://galaxy.ansible.com/infOpen/redis/)

Install redis package.

> By default, this role will also managed sysctl settings (overcommit, somaxconn) to remove warnings
> You also need Transparent Huge Pages management, see infopen.sysfs role to manage these settings per example
> I've set it for test dependencies only

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Locally, you can run tests on Docker (default driver) or Vagrant.
Travis run tests using Docker driver only.

Currently, tests are done on:
- Debian Jessie
- Ubuntu Trusty
- Ubuntu Xenial

and use:
- Ansible 2.0.x
- Ansible 2.1.x
- Ansible 2.2.x
- Ansible 2.3.x

### Running tests

#### Using Docker driver

```
$ tox
```

#### Using Vagrant driver

```
$ MOLECULE_DRIVER=vagrant tox
```

## Additional repository management

To have a more recent Redis version and have access to Sentinel on Debian Jessie, addtional repositories must be used via *redis_manage_additional_repository* variable.

You can see these repositories below, in OS distribution variables.

## Role Variables

### Default role variables

``` yaml
# General
redis_manage_system_optimization: True
redis_manage_additional_repository: True
redis_manage_redis_sentinel: False
redis_manage_redis_server: True

# Repository management
redis_apt_cache_valid_time: 3600
redis_repository_keyserver: "{{ _redis_repository_keyserver | default('') }}"
redis_repository_key_id: "{{ _redis_repository_key_id | default('') }}"
redis_repositories: "{{ _redis_repositories | default([]) }}"

# System optimization
redis_system_optimization_overcommit_memory_value: 1
redis_system_optimization_overcommit_memory_state: 'present'
redis_system_optimization_somaxconn_value: 65535
redis_system_optimization_somaxconn_state: 'present'

# System dependencies
redis_system_dependencies: "{{ _redis_system_dependencies }}"


# Redis server specific vars
#------------------------------------------------------------------------------

# Package management
redis_server_packages: "{{ _redis_server_packages }}"

# Service management
redis_server_service_name: "{{ _redis_server_service_name }}"
redis_server_service_state: 'started'
redis_server_service_enabled: True

# Files configuration
#--------------------
redis_folders: "{{ _redis_folders }}"
redis_server_config_file:
  name: 'redis.conf'
  owner: 'redis'
  group: 'redis'
  mode: '0600'

# General server configuration
redis_server_daemonize: 'yes'
redis_server_pid_file: "{{ redis_folders.pid.path }}/redis-server.pid"
redis_server_port: 6379
redis_server_bind_ip:
  - 127.0.0.1
redis_server_use_unixsocket: False
redis_server_unixsocket: "{{ redis_folders.socket.path }}/redis.sock"
redis_server_unixsocketperm: 755
redis_server_timeout: 0
redis_server_tcp_keepalive: 0
redis_server_loglevel: 'notice'
redis_server_logfile: "{{ redis_folders.log.path }}/redis-server.log"
redis_server_use_syslog: 'no'
redis_server_syslog_enabled: 'no'
redis_server_syslog_ident: 'redis'
redis_server_syslog_facility: 'local0'
redis_server_database: 16

# Snapshotting server configuration
redis_server_save:
  - '900 1'
  - '300 10'
  - '60 10000'
redis_server_stop_writes_on_bgsave_error: 'yes'
redis_server_rdbcompression: 'yes'
redis_server_rdbchecksum: 'yes'
redis_server_dbfilename: 'dump.rdb'
redis_server_dir: "{{ redis_folders.data.path }}"

# Replication configuration
redis_server_slaveof: False
redis_server_slaveof_master_ip: ''
redis_server_slaveof_master_port: ''
redis_server_master_auth: ''
redis_server_slave_serve_stale_data: 'yes'
redis_server_slave_read_only: 'yes'
redis_server_repl_ping_slave_period: 10
redis_server_repl_timeout: 60
redis_server_repl_disable_tcp_nodelay: 'no'
redis_server_repl_backlog_size: '1mb'
redis_server_repl_backlog_ttl: 3600
redis_server_slave_priority: 100
redis_server_min_slaves_to_write: 3
redis_server_min_slaves_max_lag: 10

# Security configuration
redis_server_require_pass: ''
redis_server_renamed_commands: []

# Limits configuration
redis_server_maxclients: 10000
redis_server_limit_maxmemory: False
redis_server_limit_maxmemory_size: 4000000000
redis_server_maxmemory_policy: 'volatile-lru'
redis_server_maxmemory_samples: 3

# Append only mode configuration
redis_server_appendonly: 'no'
redis_server_appendfilename: 'appendonly.aof'
redis_server_appendfsync: 'everysec'
redis_server_no_appendfsync_on_rewrite: 'no'
redis_server_auto_aof_rewrite_percentage: 100
redis_server_auto_aof_rewrite_min_size: '64mb'

# Lua scripting configuration
redis_server_lua_time_limit: 5000

# Slow log configuration
redis_server_slowlog_log_slower_than: 10000
redis_server_slowlog_max_len: 128

# Event notification configuration
redis_server_notify_keyspace_events: ''

# Advanced configuration
redis_server_hash_max_ziplist_entries: 512
redis_server_hash_max_ziplist_value: 64
redis_server_list_max_ziplist_entries: 512
redis_server_list_max_ziplist_value: 64
redis_server_set_max_intset_entries: 512
redis_server_zset_max_ziplist_entries: 128
redis_server_zset_max_ziplist_value: 64
redis_server_activerehashing: 'yes'
redis_server_client_output_buffer_limit:
  - 'normal 0 0 0'
  - 'slave 256mb 64mb 60'
  - 'pubsub 32mb 8mb 60'
redis_server_hz: 10
redis_server_aof_rewrite_incremental_fsync: 'yes'

# Includes
redis_server_include: []


# Redis sentinel specific vars
#------------------------------------------------------------------------------

# Package management
redis_sentinel_packages: "{{ _redis_sentinel_packages }}"

# Service management
redis_sentinel_service_name: "{{ _redis_sentinel_service_name }}"
redis_sentinel_service_state: 'started'
redis_sentinel_service_enabled: True

# Configuration file properties
redis_sentinel_config_file:
  name: 'sentinel.conf'
  owner: 'redis'
  group: 'redis'
  mode: '0600'

# Configuration
redis_sentinel_daemonize: True
redis_sentinel_bind: 'localhost'
redis_sentinel_port: 26379
redis_sentinel_protected_mode: True
redis_sentinel_announce_ip: null
redis_sentinel_announce_port: null
redis_sentinel_pidfile: "{{ redis_folders.pid.path }}/redis-sentinel.pid"
redis_sentinel_logfile: "{{ redis_folders.log.path }}/redis-sentinel.log"
redis_sentinel_dir: "{{ redis_folders.data.path }}"
redis_sentinel_myid: "{{ ansible_hostname | hash('sha1') }}"
redis_sentinel_monitors:
  - name: 'mymaster'
    host: '127.0.0.1'
    port: 6379
    quorum: 2
    config_epoch: 0
    down_after_milliseconds: 30000
    leader_epoch: 0
    parallel_syncs: 1
    failover_timeout: 180000
    notification_script: null
    client_reconfig_script: null
```

### Debian OS family variables

``` yaml
# Redis paths
_redis_folders:
  config:
    path: '/etc/redis'
  data:
    path: '/var/lib/redis'
  log:
    path: '/var/log/redis'
  pid:
    path: '/var/run/redis'
  socket:
    path: '/var/run/redis'


# Redis server specific vars
#------------------------------------------------------------------------------

# Packages management
_redis_server_packages:
  - name: 'redis-server'

# Service management
_redis_server_service_name: 'redis-server'


# Redis sentinel specific vars
#------------------------------------------------------------------------------

# Packages management
_redis_sentinel_packages:
  - name: 'redis-sentinel'

# Service management
_redis_sentinel_service_name: 'redis-sentinel'
```

### Ubuntu distributions variables

``` yaml
_redis_repository_keyserver: 'keyserver.ubuntu.com'
_redis_repository_key_id: 'C7917B12'
_redis_repositories:
  - repo: >
      deb http://ppa.launchpad.net/chris-lea/redis-server/{{ ansible_distribution | lower }}
      {{ ansible_distribution_release }}
      main
  - repo: >
      deb-src http://ppa.launchpad.net/chris-lea/redis-server/{{ ansible_distribution | lower }}
      {{ ansible_distribution_release }}
      main
```

### Ubuntu distributions variables

``` yaml
_redis_repository_keyserver: 'keyserver.ubuntu.com'
_redis_repository_key_id: '7E3F070089DF5277'
_redis_repositories:
  - repo: 'deb http://ftp.utexas.edu/dotdeb/ stable all'
  - repo: 'deb-src http://ftp.utexas.edu/dotdeb/ stable all'
```

## Dependencies

None

## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: infOpen.redis }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro
