import { createClient, print } from 'redis';

const client = createClient();

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (error, reply) => {
    if (error) {
      console.log('Error:', error);
    } else {
      print(`Reply: ${reply}`);
    }
  });
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, (error, value) => {
    if (error) {
      console.log('Error:', error);
    } else {
      console.log(value);
    }
  });
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
