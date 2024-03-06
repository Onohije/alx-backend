import { createClient } from 'redis';

const client = createClient();

client.on('error', function (error) {
  console.log('Redis client not connected to the server:', error);
});

client.on('connect', function () {
  console.log('Redis client connected to the server');
});
