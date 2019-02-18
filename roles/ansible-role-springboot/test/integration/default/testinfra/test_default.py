def test_port_80_is_listening(host):
  socket = host.socket("tcp://8082")
  assert(socket.is_listening)