import { createQueue } from 'kue';

const queue = createQueue();
const qName = 'push_notification_code';
const data = {
  phoneNumber: '+234 706 3491 456',
  message: 'Hello World!',
};

const job = queue.create(qName, data);
job.save();

queue.on('job enqueue', function (id, type) {
  console.log('Notification job created:', id);
});

queue.on('job complete', function (job) {
  console.log('Notification job completed');
});

queue.on('job failed', function (job, error) {
  console.log('Notification job failed');
});
