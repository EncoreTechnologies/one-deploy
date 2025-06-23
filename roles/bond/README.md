Role: opennebula.deploy.network.node
====================================

A role that manages bonds, vlans, and bridges

Requirements
------------

N/A

Role Variables
--------------

| Name                     | Type     | Default        | Example                            | Description                                   |
|--------------------------|----------|----------------|------------------------------------|-----------------------------------------------|
| `if_bonds`               | `dict`   | `{}`           | (check below)                      | Bonds to create                               |
| `if_slaves`              | `dict`   | `{}`           | (check below)                      | Slaves to bonds to create                     |
| `if_vlans`               | `dict`   | `{}`           | (check below)                      | Vlans to create                               |
| `if_bridges`             | `dict`   | `{}`           | (check below)                      | Bridges to create                             |
| `network_type`           | `str`    | `<os_default>` | `<netplan \| networkmanager>`      | Network type to use                           |
| `skip_network_node_role` | `str`    | `false`        | `true`                             | Determines to skip built in network node role |

Dependencies
------------

N/A

Notes
------------
The dict parameters for each `if_bonds`, `if_slaves`, `if_vlans`, and `if_bridges` variable corresponds to an nmcli parameter.  Any setting that does not
involve a `.` should be a simple key value pair.  Any options that involve a `.` should be placed under the `additional_config` dict which contains
a collection of dicts where the word before the `.` should be the key and the word after the `.` should be a key in the dict and the value of the option
will be the value of that key.  Ex.  if you want to set `ethernet.mtu` it would look like the following

```
...
if_slaves:
  data-bond0-p1:
    ifname: enp7s0
    type: 'ethernet'
    master: 'data-bond0'
    additional_config:
      ethernet:
        mtu: '9000'
```
Here all variables that don't involve a `.` are simple key/value and the `ethernet.mtu` variable is under `additional_config` dict

Example Playbook
----------------

    - hosts: node
      vars:
        skip_network_node_role: true # 
        if_bonds:
          data-bond0:
            mode: 802.3ad #(Optional)
            additional_config:
              connection:
                autoconnect-slaves: '1'
                autoconnect-ports: '1'
              802-3-ethernet:
                mtu: '9000'
              bond:
                miimon: '1000'
                xmit_hash_policy: 'layer3+4'
        if_slaves:
          data-bond0-p1:
            ifname: enp7s0
            type: 'ethernet'
            master: 'data-bond0'
            additional_config:
              ethernet:
                mtu: '9000'
          data-bond0-p2:
            ifname: enp8s0
            type: 'ethernet'
            master: 'data-bond0'
            additional_config:
              ethernet:
                mtu: '9000'
        if_vlans:
          data-bond0.76:
            id: 76
            dev: 'data-bond0'
            master: 'one-br0-vlan76'
            additional_config:
              ipv4:
                method: 'disabled'
              ipv6:
                method: 'disabled'
              connection:
                autoconnect: 'true'
          data-bond0.78:
            id: 78
            dev: 'data-bond0'
            master: 'one-br0-vlan78'
            additional_config:
              ipv4:
                method: 'disabled'
              ipv6:
                method: 'disabled'
              connection:
                autoconnect: 'true'
        if_bridges:
          one-br0-vlan76:
            additional_config:
              connection:
                autoconnect: true
                zone: 'public'
              ipv4:
                addresses: '172.16.76.2/24'
                method: 'manual'
              ipv6:
                method: disable
          one-br0-vlan78:
            additional_config:
              connection:
                autoconnect: true
                zone: 'public'
              ipv4:
                addresses: '172.16.78.2/24'
                method: 'manual'
              ipv6:
                method: disable
      roles:
        - role: opennebula.deploy.helper.facts
        - role: opennebula.deploy.bond

License
-------

Apache-2.0

Author Information
------------------

[OpenNebula Systems](https://opennebula.io/)
