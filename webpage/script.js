const client = mqtt.connect("mqtt://test.mosquitto.org")  // create a client

client.on("connect", () => {
  client.subscribe("monitor/sensor", (err) => {
    if (!err) {
      console.log("connected to mqtt: monitor/sensor")
    }
    else {
      console.log("error connecting to mqtt")
    }
  });
});

client.on("message", (topic, message) => {
  console.log(message.toString());
});