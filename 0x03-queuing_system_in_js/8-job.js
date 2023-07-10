export default function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) throw Error('Jobs is not an array');

  for (const job_data of jobs) {
    const job = queue.create('push_notification_code_3', job_data)
      .save((error) => {
        if (!error) console.log(`Notification job created: ${job.id}`);
      });

    job
      .on('complete', (result) => {
        console.log(`Notification job ${job.id} completed`)
      })
      .on('failed', (error) => {
        console.log(`Notification job ${job.id} failed: ${error}`)
      })
      .on('progress', (progress, data) => {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      });
  }
}
