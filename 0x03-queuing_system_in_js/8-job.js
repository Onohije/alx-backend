function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }
  for (const job_data of jobs) {
    const job = queue.create('push_notification_code_3', job_data);
    job.save((error) => {
      if (error) {
        console.log('Notification job', job.id, 'failed:', error);
      }
      console.log('Notification job created:', job.id);
    });

    job.on('complete', function () {
      console.log('Notification job', job.id, 'completed');
    });

    job.on('progress', function (progress, data) {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  }
}

export default createPushNotificationsJobs;
