import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'utils';

const app = express();
const client = createClient();

const listProducts = [
  {Id: 1, name: 'Suitcase 250', price: 50, stock: 4},
  {Id: 2, name: 'Suitcase 450', price: 100, stock: 10},
  {Id: 3, name: 'Suitcase 650', price: 350, stock: 2},
  {Id: 4, name: 'Suitcase 1050', price: 550, stock: 5}
];
const products = copyProducts();

function getItemById(id) {
  return listProducts.find((product) => product.Id === id);
}

async function reserveStockById(itemId, stock) {
  const setAsync = promisify(client.gset).bind(client);
  await setAsync(`item${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  try {
    const getAsync = promisify(client.get).bind(client);
    return (await getAsync(`item${itemId}`));
  } catch (error) {
    console.error('Redis error occurred while getting item. Error', error.message)
  }
}

function copyProducts() {
  const copy = {...listProducts};

  Object.prototype.renameKey = function (oldKey, newKey) {
    if (this.hasOwnProperty(oldKey)) {
      this[newKey] = this[oldKey];
      delete this[oldKey];
    }
    return this;
  }

  copy.map((product) => {
    product.renameKey('Id', 'itemId'));
    product.renameKey('name', 'itemName'));
    product.renameKey('stock', 'initialAvailableQuantity'));
  }

  return copy;
}

app.get('/list_products', (req, res) => {
  res.json(JSON.stringify(copyProducts()));
});

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;

  const product = getItemById(itemId);
  if (product)
    product['currentQuantity'] = await getCurrentReservedStockById(itemId);
    res.json(product);
  else
    res.json({"status":"Product not found"});
});

app.get('/reserve_product/:itemId', (req, res) => {
  const { itemId } = req.params;

  const product = getItemById(itemId);
  if (!product) {
    res.json({"status":"Product not found"});
    return;
  }

  const availableStock = await getCurrentReservedStockById(itemId);

  if (availableStock >= 1) {
    await reserveStockById(itemId, parseInt(availableStock) - 1);
    res.json({"status":"Reservation confirmed", itemId});
    return;
  } else {
    res.json({"status":"Not enough stock available", itemId});
    return;
  }
});

client
  .on('connect', () => console.log('Redis connected to server');
  .on('error', (err) => console.log('Redis couldn\'t connect to server. Error', err.message);

app.listen('1245');
