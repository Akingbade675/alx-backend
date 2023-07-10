import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();
const hgetAsync = promisify(client.hgetall).bind(client);

client.on("error", (error) => console.log(`Redis client not connected to the server: ${error.message}`));
client.on("connect", () => console.log('Redis client connected to the server'));

client.hset("HolbertonSchools", "Portland", "50", print)
client.hset("HolbertonSchools", "Seattle", "80", print)
client.hset("HolbertonSchools", "New York", "20", print)
client.hset("HolbertonSchools", "Bogota", "20", print)
client.hset("HolbertonSchools", "Cali", "40", print)
client.hset("HolbertonSchools", "Paris", "2", print)

client.hgetall("HolbertonSchools", (error, data) => {
  if (error) {
    console.error('Error retrieving value from Redis:', error.message);
    process.exit(1);
  }
  console.log(data);
});


