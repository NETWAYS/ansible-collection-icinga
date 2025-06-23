# Role netways.icinga.icingadb_redis

This role installs and configures a Redis installation specifically vendored for usage with [IcingaDB](https://icinga.com/docs/icinga-db/latest/doc/01-About/). If you are running an external Redis service or want to use a different Redis installation, you don't need to roll out this role.

> :information_source: In most scenarios you want to install the [icingadb role](../role-icingadb/) together with this role. It is part of this collection, too.


## Variables

Many variables are predefined by Icinga to make the installation easier. These are the main variables you could change.

* `icingadb_redis_binds: list`
     * Defines redis server listener, default: `["127.0.0.1","::1"]`

* `icingadb_redis_port: string`
     * Defines redis server port, default: `6380`

* `icingadb_redis_password: string`
    * Adds the `requirepass <string>` directive to Redis' configuration if set.

There is a whole set of `defaults` in place for craeting a sane Redis installation. Should you need to fine-tune settings, please consult [the defaults at `icingadb_redis/defaults/main.yml`](../../roles/icingadb_redis/defaults/main.yml) for the specific variables.
