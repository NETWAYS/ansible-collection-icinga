# Playbooks

## full_stack

The `full_stack.yml` playbook installs many Icinga components that you would typically have or want on a single-instance Icinga 2 master.  
It installs / prepares:
- Databases (using `geerlingguy.mysql`)
- Icinga repository
- NETWAYS Extras and Plugins repositories
- InfluxDB v1 (as an example TSDB)
- Monitoring Plugins
- Icinga 2
- Icinga DB Redis
- Icinga DB Daemon
- Icinga Web 2
    - Icinga DB Web
    - Icinga Director
    - Icinga Cube
    - Icinga Businessprocess
    - Performance Data Graphs

This playbook is for **demonstration purposes only!**<br>
It is meant as a showcase of what the collection can do, how a playbook might look like, and should get you a working base to play around with.

Do **not** use in production!

The playbook works on Debian / Ubuntu.

Using the playbook:<br>
Pass the target host via the variable `_target`.

```
ansible-playbook netways.icinga.full_stack -e _target=<inventory_hostname of target host>
```

> The username and password for Icinga Web 2 are `admin`.
