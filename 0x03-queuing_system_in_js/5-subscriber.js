import { createClient } from 'redis';

const sub = createClient();
const channel = 'holberton school channel';

sub.on('connect', function () {
  console.log('Redis client connected to the server');
  sub.subscribe(channel);
});

sub.on('error', function (error) {
  console.log('Redis client not connected to the server:', error);
});

sub.on('message', (channel, message) => {
  console.log(message);
  if (message === 'KILL_SERVER') {
    sub.unsubscribe(channel);
    process.exit(0);
  }
});
