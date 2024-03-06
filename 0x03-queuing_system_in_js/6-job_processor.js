import { createQueue } from 'kue';

const queue = createQueue();
const qName = 'push_notification_code';

function sendNotification(phoneNumber, message) {
  console.log('Sending notification to', phoneNumber, 'with message:', message);
}

queue.process(qName, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message);
  done();
});
