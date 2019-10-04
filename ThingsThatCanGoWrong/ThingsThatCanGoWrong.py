# This is a kind of check list to know which labes are validate and which one can go wrong and need to validate
# The values of dictionary are 3 types:
#   CHECK: That means the script can validate it. Yeay! :)
#   TODO: Means the script not validate it completly or at all! :(
#   UNKNOWN: It can go wrong but someone who use this lable, knows what's he doing!


issues = {
    'Duplicate service name' : 'CHECK',
    'Typing mistake': 'CHECK',
    # 'top-level property': 'CHECK', # version, services, networks, volumes     It's not important!
    'extensions starting with x-': 'TODO', #Version 3.4 or higher
    'Duplicate container name' : 'CHECK',
    'NETWORK NAME': 'TODO',
    'Duplicate image' : 'CHECK',
    'Duplicate Key in docker compose': 'CHECK',
    'Duplicate port' : 'CHECK',
    'expose' : 'CHECK',
    'Invalid volume directory' : 'CHECK', # Only for github and CLI. mostly working
    'build label and all it needs' : 'TODO', # Including: build, CONTEXT, DOCKERFILE, ARGS, CACHE_FROM, LABELS, SHM_SIZE, TARGET
    # Build path is only for github links and CLI
    'image lable' : 'TODO',
    'other versions of compose' : 'TODO',  # Lastest version can cover older versions, right? :)
    'local use' : 'TODO',
    'good file-based reporting' : 'TODO',
    'depends_on' : 'CHECK',
    'credential_spec' : 'TODO',
    'configs' : 'TODO',
    'deploy' : 'TODO', # It's version 3 only
    'ENDPOINT_MODE' : 'TODO', # Only in versio 3.3
    'LABELS' : 'TODO',
    'MODE' : 'TODO',
    'PLACEMENT' : 'TODO',
    'REPLICAS' : 'TODO',
    'RESOURCES' : 'TODO',
    'RESTART_POLICY' : 'TODO',
    'UPDATE_CONFIG' : 'TODO',
    'devices' : 'TODO',
    'dns' : 'CHECK',
    'dns_search' : 'TODO',
    'entrypoint' : 'TODO',
    'env_file' : 'TODO',
    'external_links' : 'TODO',
    'extra_hosts' : 'TODO',
    'healthcheck' : 'TODO',
    'init' : 'TODO', # This is very new! :)
    'links' : 'UNKNOWN',
    'isolation' : 'UNKNOWN',
    'logging' : 'UNKNOWN',
    'network_mode' : 'TODO',
    'networks' : 'TODO',
    'secrets' : 'UNKNOWN',
    'security_opt' : 'TODO',
    'sysctls' : 'UNKNOWN',
    'tmpfs' : 'TODO',
    'stop_signal' : 'UNKNOWN',
    'ulimits' : 'UNKNOWN',
    'Some single values' : 'TODO', # domainname, hostname, ipc, mac_address, privileged, read_only, shm_size, stdin_open, tty, user, working_dir
    'ipam' : 'TODO',
    'Variable substitution' : 'TODO',
    'Extension fields' : 'TODO',
    
}