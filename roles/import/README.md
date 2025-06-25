Role: opennebula.deploy.kvm
===========================

A role that manages importing existing networks and vms into frontend opennebula

Requirements
------------

N/A

Role Variables
--------------

| Name                      | Type    | Default                     | Description                                                               | 
|---------------------------|---------|-----------------------------|---------------------------------------------------------------------------|
| `oneimage_datastore_name` | `str`   | `default`                   | The name or id of the datastore to use when "oneimage create" is used     |           
| `one_tmp_dir`             | `str`   | `/var/tmp/one`              | Directory where network and vm template are generated                     | 
| `vm_register_retries`     | `int`   | `5`                         | Number of retries to wait for vm to register.  More below                 |
| `vm_register_delay`       | `int`   | `5`                         | Number in seconds to delay between retries.  More below                   |  
| `vms_to_import`           | `dict`  | `[]`                        | Dict of vms to import.  This should be placed                             |
|                           |         |                             | per node                                                                  |
|                           |         |                             | in inventory file                                                         | 
| `vlans_to_import`         | `dict`  | `{}`                        | The vlans on node to import. This should be placed per node in            |
|                           |         |                             | inventory file                                                            |
| `native_vlans_to_import`  | `dict`  | `{}`                        | The native vlans on node to import. This should be placed per node in     |
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

When the role begins to copy over disks from vm, things will hang until they are copied over.  In order to view the status of the transfer,
you can tail the logs at `/var/tmp/one/logs/<vm_name>/<disk_name>.log`

Vlans
-----
Both `vlans_to_import` and `native_vlans_to_import` are dicts where the key is name of the network to import and the value is dict with following keys:
  - template_name: Name to use for network in opennebula
  - mac_ar_size: The size of the mac address range to use for network when importing

Example:
```
vlans_to_import
  bond0.68:
    template_name: vlan_68_test_10_0_68_network
  bond0.86:
    template_name: vlan_86_test_10_0_86_network
    mac_ar_size: 200
```

VMs
---
The `vms_to_import` variable is a list of dicts that determines what vms to import into the frontend.  The name in each object must match the name
that is displayed in `virsh`.

The values are as follows:
- <key_name>: The name of vm to import seen in `virsh`
  - pinned_host (Optional): FQDN of the host you want to pin the vm to
  - prevent_start_on_import (Optional): Bool that determines if user wants to stop the vm from initiating on newly imported vm

Example:
```
vms_to_import
  wild1_vm_name:
    pinned_host: onhv-01.example.com
    prevent_start_on_import: true
  wild2_vm_name:
    pinned_host: onhv-01.example.com
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
