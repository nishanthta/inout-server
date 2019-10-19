const { MongoClient, Logger } = require("mongodb");

const getDatabase = async () => {
  const url = 'mongodb://localhost:27017';
  const client = new MongoClient(url, { useNewUrlParser: true });

  let logCount = 0;
  Logger.setCurrentLogger(msg => {
    console.log(`MONGO DB REQUEST ${++logCount}: ${msg}`);
  });
  Logger.setLevel("debug");
  Logger.filter("class", ["Cursor"]);

  try {
    await client.connect();
    return client.db('bubblegum');
  } catch (err) {
    throw err;
  }
};

module.exports = { getDatabase };