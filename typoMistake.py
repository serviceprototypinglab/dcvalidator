tags = {
    'general':
        [
            'version',
            'services',
            'networks',
            'volumes',
            'configs',
            'secrets',
        ],
    'service':
        [
            'build',
            'cap_add',
            'cap_drop',
            'cgroup_parent',
            'command',
            'container_name',
            'credential_spec',
            'config',
            'depends_on',
            'deploy',
            'devices',
            'dns',
            'dns_search',
            'entrypoint',
            'env_file',
            'environment',
            'expose',
            'external_links',
            'extra_hosts',
            'healthcheck',
            'image',
            'init',
            'isolation',
            'labels',
            'links',
            'logging',
            'network_mode',
            'networks',
            'pid',
            'ports',
            'restart',
            'secrets',
            'security_opt',
            'stop_grace_period',
            'stop_signal',
            'sysctls',
            'tmpfs',
            'ulimits',
            'userns_mode',
            'volumes',
        ],
    'build':
        [
            'context',
            'dockerfile',
            'args',
            'buildno',
            'image',
            'gitcommithash',
            'cache_from',
            'labels',
            'shm_size',
            'target',
        ],
    'config':
        [
            'source',
            'target',
            'uid',
            'gid',
            'mode',
        ],
    'deploy':
        [
            'mode',
            'endpoint_mode',
            'replicas',
            'labels',
            'placement',
            'resources',
            'restart_policy',
            'update_config',
            'rollback_config',
        ],
    'network':
        [
            'aliases',
            'ipv4_address',
            'ipv6_address',
        ],

    'ports':
        [
            'target',
            'published',
            'protocol',
            'mode',
        ],
    'secret':
        [
            'source',
            'target',
            'uid',
            'gid',
            'mode',
        ],
    'volumes':
        [
            'type',
            'source',
            'target',
            'read_only',
            'bind',
            'propagation',
            'volume',
            'nocopy',
            'tmpfs',
            'size',
            'consistency',
        ]
}

'''
general_property_tags = [
    'version',
    'services',
    'networks',
    'volumes',
    'configs',
    'secrets',

]

service_property_tags = [
    'build',
    'cap_add',
    'cap_drop',
    'cgroup_parent',
    'command',
    'container_name',
    'credential_spec',
    'config',
    'depends_on',
    'deploy',
    'devices',
    'dns',
    'dns_search',
    'entrypoint',
    'env_file',
    'environment',
    'expose',
    'external_links',
    'extra_hosts',
    'healthcheck',
    'image',
    'init',
    'isolation',
    'labels',
    'links',
    'logging',
    'network_mode',
    'networks',
    'pid',
    'ports',
    'restart',
    'secrets',
    'security_opt',
    'stop_grace_period',
    'stop_signal',
    'sysctls',
    'tmpfs',
    'ulimits',
    'userns_mode',
    'volumes',

]

build_property_tags = [
    'context',
    'dockerfile',
    'args',
    'buildno',
    'image',
    'gitcommithash',
    'cache_from',
    'labels',
    'shm_size',
    'target',
]

config_property_tags = [

]

deploy_property_tags = [
    'mode',
    'endpoint_mode',
    'replicas',
    'labels',
    'placement',
    'resources',
    'restart_policy',
    'update_config',
    'rollback_config',

]


network_property_tags = [
    'aliases',
    'ipv4_address',
    'ipv6_address',

]

ports_property_tags = [
    'target',
    'published',
    'protocol',
    'mode',
]

secret_property_tags = [
    'source',
    'target',
    'uid',
    'gid',
    'mode',
]

volumes_property_tags = [
    'type',
    'source',
    'target',
    'read_only',
    'bind',
    'propagation',
    'volume',
    'nocopy',
    'tmpfs',
    'size',
    'consistency',
]
'''