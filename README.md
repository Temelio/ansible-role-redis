# redis

[![Build Status](https://travis-ci.org/infOpen/ansible-role-redis.svg?branch=master)](https://travis-ci.org/infOpen/ansible-role-redis)

Install redis package.

## Requirements

This role requires Ansible 2.0 or higher,
and platform requirements are listed in the metadata file.

## Testing

This role contains two tests methods :
- locally using Vagrant
- automatically with Travis

### Testing dependencies
- install [Vagrant](https://www.vagrantup.com)
- install [Vagrant serverspec plugin](https://github.com/jvoorhis/vagrant-serverspec)
    $ vagrant plugin install vagrant-serverspec
- install ruby dependencies
    $ bundle install

### Running tests

#### Run playbook and test

- if Vagrant box not running
    $ vagrant up

- if Vagrant box running
    $ vagrant provision

## Role Variables

### Default role variables

    # Firewall configuration
    #-----------------------
    redis_firewall_managed_with_ferm: False
    redis_ferm_input_rules_file: '/etc/ferm/input/redis.conf'
    redis_ferm_files_owner: 'root'
    redis_ferm_files_group: 'root'
    redis_ferm_files_mode: '0400'
    redis_ferm_main_config_file: '/etc/ferm/ferm.conf'
    redis_ferm_service_name: 'ferm'
    redis_ferm_input_rules:
      - 'proto tcp mod tcp dport 6379 ACCEPT;'

## Dependencies

### Mandatory dependencies

None

### Optional dependencies

- Temelio.ferm

## Example Playbook

    - hosts: servers
      roles:
         - { role: infOpen.redis }

## License

MIT

## Author Information

Alexandre Chaussier (for Infopen company)
- http://www.infopen.pro
- a.chaussier [at] infopen.pro

