import { createClient, print } from 'redis';

const client = createClient();

client
  .on("error", (error) => {
    console.log(`Redis client not connected to the server: ${error.message}`)
  })
  .on("connect", () => console.log('Redis client connected to the server'));

client.subscribe("holberton school channel", (channel, message) => {
  if(message === "KILL_SERVER") {
    console.log(channel);
    client.unsubscribe(channel);
    client.quit();
  } else {
    console.log(message);
  }
});
