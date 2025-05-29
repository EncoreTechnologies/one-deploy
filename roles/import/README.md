Role: opennebula.deploy.kvm
===========================

A role that manages OpenNebula KVM Nodes/Hosts.

Requirements
------------

N/A

Role Variables
--------------

| Name                      | Type    | Default                     | Description                                                               | 
|---------------------------|---------|-----------------------------|---------------------------------------------------------------------------|
| `oneimage_datastore_name` | `str`   | `default`                   | The name or id of the datastore to use when "oneimage create" is used     | 
| `oneimage_datastore_dir`  | `str`   | `/var/lib/one/datastores/1` | The default location to import disks to on frontend                       | 
| `node_datastore_dir`      | `str`   | `/var/lib/one/datastores/0` | Root directory on node where the copied over disks will be backed up to   |            
| `one_tmp_dir`             | `str`   | `/var/tmp/one`              | Directory where network and vm template are generated                     | 
| `vm_register_retries`     | `int`   | `5`                         | Number of retries to wait for vm to register.  More below                 |
| `vm_register_delay`       | `int`   | `5`                         | Number in seconds to delay between retries.  More below                   |  
| `vms_to_import`           | `list`  | `[]`                        | The vms to import and must be running.  This should be placed per node    |
|                           |         |                             | in inventory file                                                         | 
| `vlans_to_import`         | `list`  | `[]`                        | The vlans on node to import. This should be placed per node in            |
|                           |         |                             | inventory file                                                            |
| `native_vlans_to_import`  | `list`  | `[]`                        | The native vlans on node to import. This should be placed per node in     |
|                           |         |                             | inventory file                                                            |
| `vn_mac_ar_size`          | `int`   | `254`                       | The size of the mac address space for a network                           |

Notes
-----
The reason for the `vm_register_retries` and `vm_register_delay` variables is that once a host is created, there is a delay
on when the info is actually displayed to user so we must repeatedly query for the vm info on the host.  The default of
`25` total seconds should be good since we also do a `onehost forceupdate <host>` right before we begin querying to force the monitoring
system to update quicker.

There is a dedicated playbook for this role in the `playbooks` directory.  When using the playbook, it is advised to use `--skip-tags` for
the `libvirt` section of the play to avoid any unesscary updates on the existing nodes as we use part of the `kvm` role to set things up for
the import

Example 
```
ansible-playbook -i inventory.yml -v opennebula.deploy.import --skip-tags libvirt
```

Vlans
-----
Both `vlans_to_import` and `native_vlans_to_import` are a list of dicts where the keys we have are:
  - name: Name of network to import
  - mac_ar_size: The size of the mac address range to use for network when importing

Example:
```
vlans_to_import = [{'name': 'one-br-vlan76', 'mac_ar_size': 254}]
```

Example Playbook
----------------
```
- hosts: node
  collections:
    - opennebula.deploy
  roles:
    - role: common
    - role: helper/facts
    - role: kvm
    - role: import
```
License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
