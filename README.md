# microservices-demo-ansible

This is a demo of deploying springboot microservices using ansible. More significanly it has logic to [move springboot microservices between hosts](https://devops.stackexchange.com/q/6393/10599). 

The role in this repos is derived from [ansible-role-springboot](https://github.com/orachide/ansible-role-springboot). It has some modifications to so that rather than `sb_app_state` being static, or defined per hosts or group, it is computed from a new varaible `sb_hosts`. This 

See `playbook-install.yml` that instals two microservices on the same machine which has something like this:

```
roles:
    - {
      role: "ansible-role-springboot",
      sb_app_name: "microservices-registration",
      sb_app_group_id: "org.springframework.samples.service.service",
      sb_app_artifact_id: "microservices-demo",
      sb_app_version: "2.0.0.RELEASE",
      sb_app_run_args: '"registration 8082"',
      sb_app_healthcheck_urls: [
        "http://localhost:8082/actuator/health"
      ],
      sb_hosts: [
        "my-test-vm"
      ]
    }
    - {
      role: "ansible-role-springboot",
      sb_app_name: "microservices-web",
      sb_app_group_id: "org.springframework.samples.service.service",
      sb_app_artifact_id: "microservices-demo",
      sb_app_version: "2.0.1.RELEASE",
      sb_app_run_args: '"web 8083"',
      sb_app_healthcheck_urls: [
        "http://localhost:8083/actuator/health"
      ],
      sb_hosts: [
        "not-current-host.example.com"
      ]
    }
```

Note that the two different applications of the same roles deploy different springboot microservies onto different `sb_hosts` host list. If you add or remove hosts from the lists the service will be installed or uninstalled. 

Note that with springboot you can have your processes automaticallly register themselves with Eureka for service discovery. You can also use ribbon for client side loadbalancing and breakers. That should make it reasonablly safe to dynamically move one of many microservices between hosts but YMMV. 

## Set up on macos

Running a load of infrastructure to test things is hard work. So I am using test-kitchen to test deploying to linux VMs running under Vagrant on my macbook as per https://medium.com/@Joachim8675309/testkitchen-with-ansible-and-testinfra-e3fc4320ced 

Roughly this is the setup I did as per that article or the other articles that it linked to: 

```
# install chef sdk
chef gem install kitchen-ansible
sudo gem install test-kitchen
sudo gem install kitchen-vagrant
sudo gem install kitchen-ansible

sudo pip install --upgrade pip
sudo pip install tornado nose
sudo pip install testinfra
sudo pip install paramiko

brew cask install vagrant
vagrant plugin expunge --reinstall
```

## Running

Go into `roles/ansible-role-springboot` and run `kitchen converge && kitchen verify` to see it install and run tests. Then you can run  `kitchen login` to ssh in and have a look around. If you run `kitchen test` it will destroy the VM which is fine for unit testing but slower than doing an incremental verify. 
