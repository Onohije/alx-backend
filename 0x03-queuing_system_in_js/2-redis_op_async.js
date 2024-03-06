import { createClient, print } from 'redis';

const util = require('util');
const client = createClient();
const get = util.promisify(client.get).bind(client);

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (error, reply) => {
    if (error) {
      console.log('Error:', error);
    } else {
      print(`Reply: ${reply}`);
    }
  });
}

async function displaySchoolValue(schoolName) {
  try {
    const name = await get(schoolName);
    console.log(name);
  } catch (error) {
    console.log('Error:', error);
  }
}

client.on('error', function (error) {
  console.log('Redis client not connected to the server:', error);
});

client.on('connect', function () {
  console.log('Redis client connected to the server');
  displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  displaySchoolValue('HolbertonSanFrancisco');
});
