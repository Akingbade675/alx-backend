import express from 'express';
import { promisify } from 'util';
import redis from 'redis';
import kue from 'kue';

const app = express();
const port = 1245;
const client = redis.createClient();
const queue = kue.createQueue();


let reservationEnabled = true;
let numberOfAvailableSeats = 50;


const reserveSeat = async (number) => {
  const setAsync = promisify(client.set).bind(client);
  await setAsync('available_seats', number);
};


const getCurrentAvailableSeat = async (itemId) => {
  const getAsync = promisify(client.get).bind(client);
  const noOfSeats = await getAsync('available_seats');
  return noOfSeats ? noOfSeats : '0';
};


app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeat();
  res.json({'numberOfAvailableSeats': seats});
});


app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ 'status': 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save(err => {
    if (err)
      res.json({ 'status': 'Reservation failed' });
    else
      res.json({ 'status': 'Reservation in process' });
  });
});


app.get('/process', (req, res) => {
  res.json({ 'status': 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeat();
    const newSeats = parseInt(currentSeats) - 1;

    if (newSeats >= 0) {
      await reserveSeat(newSeats);
      numberOfAvailableSeats = newSeats;

      if (newSeats === 0) reservationEnabled = false;

      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});


queue.on('job complete', (id) => {
  console.log(`Seat reservation job ${id} completed`);
});
    
queue.on('job failed', (id, err) => {
  console.log(`Seat reservation job ${jid} failed: ${err.message}`);
});


app.listen(port, async () => {
  console.log(`Server is running on port ${port}`);
  await reserveSeat(numberOfAvailableSeats);
});
