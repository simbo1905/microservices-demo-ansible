# microservices-demo-ansible

This is a demo of deploying springboot microservices using ansible. 

In a typically scenario there will be snapshot builds on a private repo nexus. So this project deploys jars that are published on github under the project https://github.com/simbo1905/microservices-demo

The role in this repos is derived from [ansible-role-springboot](https://github.com/orachide/ansible-role-springboot).

It modifies that role so that rather than `sb_app_state` being static, or defined on hosts, or groups of hosts, it is computed from a new varaible `sb_hosts` using the script `host_test.sh`. This script checks `hostname -f` appears in `sb_hosts`. It then sets  `sb_app_state` to either install or uninstall the app. The idea being that to move one instance of a microservice we need to run on the host we are added to and also the host we are removing it from. This means that we have to run agaisnt all our hosts. Having the explists list right there were we invoke the role makes it easier to see what service is defined where:

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

## What Next?

Moving a microservice needs a fact and a role. 