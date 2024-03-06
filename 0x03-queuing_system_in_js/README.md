Node-Redis
Tests Coverage License

Discord Twitch YouTube Twitter

node-redis is a modern, high performance Redis client for Node.js.

How do I Redis?
Learn for free at Redis University

Build faster with the Redis Launchpad

Try the Redis Cloud

Dive in developer tutorials

Join the Redis community

Work at Redis

Packages
Name	Description
redis	Downloads Version
@redis/client	Downloads Version Docs
@redis/bloom	Downloads Version Docs Redis Bloom commands
@redis/graph	Downloads Version Docs Redis Graph commands
@redis/json	Downloads Version Docs Redis JSON commands
@redis/search	Downloads Version Docs RediSearch commands
@redis/time-series	Downloads Version Docs Redis Time-Series commands
⚠️ In version 4.1.0 we moved our subpackages from @node-redis to @redis. If you're just using npm install redis, you don't need to do anything—it'll upgrade automatically. If you're using the subpackages directly, you'll need to point to the new scope (e.g. @redis/client instead of @node-redis/client).

Installation
Start a redis via docker:

docker run -p 6379:6379 -it redis/redis-stack-server:latest
To install node-redis, simply:

npm install redis
⚠️ The new interface is clean and cool, but if you have an existing codebase, you'll want to read the migration guide.

Looking for a high-level library to handle object mapping? See redis-om-node!

Usage
Basic Example
import { createClient } from 'redis';

const client = await createClient()
  .on('error', err => console.log('Redis Client Error', err))
  .connect();

await client.set('key', 'value');
const value = await client.get('key');
await client.disconnect();
The above code connects to localhost on port 6379. To connect to a different host or port, use a connection string in the format redis[s]://[[username][:password]@][host][:port][/db-number]:

createClient({
  url: 'redis://alice:foobared@awesome.redis.server:6380'
});
You can also use discrete parameters, UNIX sockets, and even TLS to connect. Details can be found in the client configuration guide.

To check if the the client is connected and ready to send commands, use client.isReady which returns a boolean. client.isOpen is also available. This returns true when the client's underlying socket is open, and false when it isn't (for example when the client is still connecting or reconnecting after a network error).

Redis Commands
There is built-in support for all of the out-of-the-box Redis commands. They are exposed using the raw Redis command names (HSET, HGETALL, etc.) and a friendlier camel-cased version (hSet, hGetAll, etc.):

// raw Redis commands
await client.HSET('key', 'field', 'value');
await client.HGETALL('key');

// friendly JavaScript commands
await client.hSet('key', 'field', 'value');
await client.hGetAll('key');
Modifiers to commands are specified using a JavaScript object:

await client.set('key', 'value', {
  EX: 10,
  NX: true
});
Replies will be transformed into useful data structures:

await client.hGetAll('key'); // { field1: 'value1', field2: 'value2' }
await client.hVals('key'); // ['value1', 'value2']
Buffers are supported as well:

await client.hSet('key', 'field', Buffer.from('value')); // 'OK'
await client.hGetAll(
  commandOptions({ returnBuffers: true }),
  'key'
); // { field: <Buffer 76 61 6c 75 65> }
Unsupported Redis Commands
If you want to run commands and/or use arguments that Node Redis doesn't know about (yet!) use .sendCommand():

await client.sendCommand(['SET', 'key', 'value', 'NX']); // 'OK'

await client.sendCommand(['HGETALL', 'key']); // ['key1', 'field1', 'key2', 'field2']
Transactions (Multi/Exec)
Start a transaction by calling .multi(), then chaining your commands. When you're done, call .exec() and you'll get an array back with your results:

await client.set('another-key', 'another-value');

const [setKeyReply, otherKeyValue] = await client
  .multi()
  .set('key', 'value')
  .get('another-key')
  .exec(); // ['OK', 'another-value']
You can also watch keys by calling .watch(). Your transaction will abort if any of the watched keys change.

To dig deeper into transactions, check out the Isolated Execution Guide.

Blocking Commands
Any command can be run on a new connection by specifying the isolated option. The newly created connection is closed when the command's Promise is fulfilled.

This pattern works especially well for blocking commands—such as BLPOP and BLMOVE:

import { commandOptions } from 'redis';

const blPopPromise = client.blPop(
  commandOptions({ isolated: true }),
  'key',
  0
);

await client.lPush('key', ['1', '2']);

await blPopPromise; // '2'
To learn more about isolated execution, check out the guide.

Pub/Sub
See the Pub/Sub overview.

Scan Iterator
SCAN results can be looped over using async iterators:

for await (const key of client.scanIterator()) {
  // use the key!
  await client.get(key);
}
This works with HSCAN, SSCAN, and ZSCAN too:

for await (const { field, value } of client.hScanIterator('hash')) {}
for await (const member of client.sScanIterator('set')) {}
for await (const { score, value } of client.zScanIterator('sorted-set')) {}
You can override the default options by providing a configuration object:

client.scanIterator({
  TYPE: 'string', // `SCAN` only
  MATCH: 'patter*',
  COUNT: 100
});
Programmability
Redis provides a programming interface allowing code execution on the redis server.

Functions
The following example retrieves a key in redis, returning the value of the key, incremented by an integer. For example, if your key foo has the value 17 and we run add('foo', 25), it returns the answer to Life, the Universe and Everything.

#!lua name=library

redis.register_function {
  function_name = 'add',
  callback = function(keys, args) return redis.call('GET', keys[1]) + args[1] end,
  flags = { 'no-writes' }
}
Here is the same example, but in a format that can be pasted into the redis-cli.

FUNCTION LOAD "#!lua name=library\nredis.register_function{function_name=\"add\", callback=function(keys, args) return redis.call('GET', keys[1])+args[1] end, flags={\"no-writes\"}}"
Load the prior redis function on the redis server before running the example below.

import { createClient } from 'redis';

const client = createClient({
  functions: {
    library: {
      add: {
        NUMBER_OF_KEYS: 1,
        transformArguments(key: string, toAdd: number): Array<string> {
          return [key, toAdd.toString()];
        },
        transformReply(reply: number): number {
          return reply;
        }
      }
    }
  }
});

await client.connect();

await client.set('key', '1');
await client.library.add('key', 2); // 3
Lua Scripts
The following is an end-to-end example of the prior concept.

import { createClient, defineScript } from 'redis';

const client = createClient({
  scripts: {
    add: defineScript({
      NUMBER_OF_KEYS: 1,
      SCRIPT:
        'return redis.call("GET", KEYS[1]) + ARGV[1];',
      transformArguments(key: string, toAdd: number): Array<string> {
        return [key, toAdd.toString()];
      },
      transformReply(reply: number): number {
        return reply;
      }
    })
  }
});

await client.connect();

await client.set('key', '1');
await client.add('key', 2); // 3
Disconnecting
There are two functions that disconnect a client from the Redis server. In most scenarios you should use .quit() to ensure that pending commands are sent to Redis before closing a connection.

.QUIT()/.quit()
Gracefully close a client's connection to Redis, by sending the QUIT command to the server. Before quitting, the client executes any remaining commands in its queue, and will receive replies from Redis for each of them.

const [ping, get, quit] = await Promise.all([
  client.ping(),
  client.get('key'),
  client.quit()
]); // ['PONG', null, 'OK']

try {
  await client.get('key');
} catch (err) {
  // ClosedClient Error
}
.disconnect()
Forcibly close a client's connection to Redis immediately. Calling disconnect will not send further pending commands to the Redis server, or wait for or parse outstanding responses.

await client.disconnect();
Auto-Pipelining
Node Redis will automatically pipeline requests that are made during the same "tick".

client.set('Tm9kZSBSZWRpcw==', 'users:1');
client.sAdd('users:1:tokens', 'Tm9kZSBSZWRpcw==');
Of course, if you don't do something with your Promises you're certain to get unhandled Promise exceptions. To take advantage of auto-pipelining and handle your Promises, use Promise.all().

await Promise.all([
  client.set('Tm9kZSBSZWRpcw==', 'users:1'),
  client.sAdd('users:1:tokens', 'Tm9kZSBSZWRpcw==')
]);
Clustering
Check out the Clustering Guide when using Node Redis to connect to a Redis Cluster.

Events
The Node Redis client class is an Nodejs EventEmitter and it emits an event each time the network status changes:

Name	When	Listener arguments
connect	Initiating a connection to the server	No arguments
ready	Client is ready to use	No arguments
end	Connection has been closed (via .quit() or .disconnect())	No arguments
error	An error has occurred—usually a network issue such as "Socket closed unexpectedly"	(error: Error)
reconnecting	Client is trying to reconnect to the server	No arguments
sharded-channel-moved	See here	See here
⚠️ You MUST listen to error events. If a client doesn't have at least one error listener registered and an error occurs, that error will be thrown and the Node.js process will exit. See the EventEmitter docs for more details.

The client will not emit any other events beyond those listed above.

Supported Redis versions
Node Redis is supported with the following versions of Redis:

Version	Supported
7.0.z	✔️
6.2.z	✔️
6.0.z	✔️
5.0.z	✔️
< 5.0	❌
Node Redis should work with older versions of Redis, but it is not fully tested and we cannot offer support.

Contributing
If you'd like to contribute, check out the contributing guide.

Thank you to all the people who already contributed to Node Redis
