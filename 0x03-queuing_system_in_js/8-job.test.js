import { createQueue } from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-jobs.js';

const queue = createQueue();

describe('#createPushNotificationsJobs', () => {
  before(() => {
    queue.testMode.enter();
  });

  after(() => {
    queue.testMode.exit();
  });

  beforeEach(() => {
    queue.testMode.clear();
  });

  it('display a error message if jobs is not an array', () => {
    const fn = createPushNotificationsJobs.bind(this, "send", queue);
    expect(fn).to.throw('Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {
    const job_data = [
      {
        phoneNumber: '456754890',
        message: 'Send money delivered notification'
      },
      {
        phoneNumber: '458914450',
        message: 'Send money delivered notification'
      },
    ];

    createPushNotificationsJobs(job_data, queue);

    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[1].phoneNumber).to.equal('458914450');
  });

});
