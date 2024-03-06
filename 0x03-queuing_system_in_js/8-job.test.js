import createPushNotificationsJobs from './8-job';
import { createQueue } from 'kue';

const assert = require('assert');
const queue = createQueue();

const jobs = [
  {
    phoneNumber: '4154318781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account',
  },
];

describe('Test createPushNotificationsJobs', function () {
  before(function () {
    queue.testMode.enter();
  });

  afterEach(function () {
    queue.testMode.clear();
  });

  after(function () {
    queue.testMode.exit();
  });

  it('displays an error message if jobs is not an array', function () {
    assert.throws(() => createPushNotificationsJobs(jobs[0], queue), Error);
  });

  it('creates two new jobs in queue', function () {
    createPushNotificationsJobs(jobs, queue);
    assert.equal(queue.testMode.jobs.length, 2);
  });
});
