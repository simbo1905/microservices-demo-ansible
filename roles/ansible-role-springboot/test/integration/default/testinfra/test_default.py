def test_port_8082_is_listening(host):
  socket = host.socket("tcp://8082")
  assert(socket.is_listening)

def test_microservices_demo_running_and_enabled(host):
    microservice = host.service("microservices-demo")
    assert microservice.is_running
    assert microservice.is_enabled