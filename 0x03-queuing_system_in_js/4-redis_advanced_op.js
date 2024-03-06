import { createClient, print } from 'redis';

const client = createClient();

const key = 'HolbertonSchools';
const hash_set = [
  ['Portland', 50],
  ['Seattle', 80],
  ['New York', 20],
  ['Bogota', 20],
  ['Cali', 40],
  ['Paris', 2],
];

function main() {
  for (const set of hash_set) {
    client.hset(key, set[0], set[1], (error, reply) => {
      if (error) {
        console.log('Error:', error);
      } else {
        print(`Reply: ${reply}`);
      }
    });
  }
  client.hgetall(key, (error, reply) => {
    if (error) {
      console.log('Error:', error);
    } else {
      console.log(reply);
    }
  });
}

client.on('connect', function () {
  console.log('Redis client connected to the server');
  main();
});

client.on('error', function (error) {
  console.log('Redis client not connected to the server:', error);
});
