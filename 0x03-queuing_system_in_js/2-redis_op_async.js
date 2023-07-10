import { createClient, print } from 'redis';
import { promisify } from 'util';

const client = createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

client.on("error", (error) => console.log(`Redis client not connected to the server: ${error.message}`));
client.on("connect", () => console.log('Redis client connected to the server'));

async function setNewSchool(schoolName, value) {
  try {
    const reply = await setAsync(schoolName, value);
    print(reply)
  } catch (error) {
    console.error('Error setting value in Redis:', error.message);
  }
}

async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (error) {
    console.error('Error retrieving value from Redis:', error.message);
  }
}


displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
