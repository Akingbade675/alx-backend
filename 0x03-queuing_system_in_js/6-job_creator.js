import { createQueue } from 'kue';

console.log('QUEUE');
const queue = createQueue();
const job_data = {
  phoneNumber: "01 938 8378",
  message: "Call me back when less busy",
};

const job = queue.create(
  'push_notification_code',
  job_data
).save((err) => {
  console.log(`Notification job created: ${job.id}`);
});

job
  .on('complete', (result) => console.log('Notification job completed'))
  .on('failed', (result) => console.log('Notification job failed'));
