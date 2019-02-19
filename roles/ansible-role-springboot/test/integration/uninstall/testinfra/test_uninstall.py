def test_port_8082_is_listening(host):
  socket = host.socket("tcp://8082")
  assert(socket.is_listening)

def test_port_8083_is_listening(host):
  socket = host.socket("tcp://8083")
  assert socket.is_listening == False

def test_microservices_registration_running_and_enabled(host):
    microservice = host.service("microservices-registration")
    assert microservice.is_running
    assert microservice.is_enabled

def test_microservices_web_running_and_enabled(host):
    microservice = host.service("microservices-web")
    assert microservice.is_enabled == False

def test_microservices_registration_version(host):
    microservice = host.process.get(user="sbuser", comm="MICROSERVICES-R")
    assert microservice.pid > 0
    workers = host.process.filter(ppid=microservice.pid)
    assert len(workers) == 1
    assert "2.0.0.RELEASE" in workers[0].args 

def test_microservices_web_version(host):
    microservice = True
    try: host.process.get(user="sbuser", comm="MICROSERVICES-W")
    except RuntimeError: microservice = None
    assert microservice == None    

