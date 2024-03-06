import { createClient } from 'redis';

const pub = createClient();
const channel = 'holberton school channel';

function publishMessage(message, time) {
  setTimeout(() => {
    console.log('About to send', message);
    pub.publish(channel, message);
  }, time);
}

pub.on('error', function (error) {
  console.log('Redis client not connected to the server:', error);
});

pub.on('connect', function () {
  console.log('Redis client connected to the server');
  publishMessage('Holberton Student #1 starts course', 100);
  publishMessage('Holberton Student #2 starts course', 200);
  publishMessage('KILL_SERVER', 300);
  publishMessage('Holberton Student #3 starts course', 400);
});
