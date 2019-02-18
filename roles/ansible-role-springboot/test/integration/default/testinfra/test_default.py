def test_port_8082_is_listening(host):
  socket = host.socket("tcp://8082")
  assert(socket.is_listening)

def test_port_8083_is_listening(host):
  socket = host.socket("tcp://8083")
  assert(socket.is_listening)

def test_microservices_registration_running_and_enabled(host):
    microservice = host.service("microservices-registration")
    assert microservice.is_running
    assert microservice.is_enabled

def test_microservices_web_running_and_enabled(host):
    microservice = host.service("microservices-web")
    assert microservice.is_running
    assert microservice.is_enabled