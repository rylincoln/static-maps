const express = require("express");
const app = express();
const cors = require("cors");
const helmet = require("helmet");
require("dotenv").config();

const findRemoveSync = require('find-remove')
const schedule = require('node-schedule');


var j = schedule.scheduleJob('*/15 * * * *', function () {
    const result = findRemoveSync(__dirname + '/public', {
        extensions: ['.png']
    })
    console.log('removing png images and icons')
});

app.use(express.json({limit: '50mb'}));
app.use(express.urlencoded({limit: '50mb', extended: true}));

app.use(express.static('public'))
app.use('/icons', express.static('icons'))

app.use(cors());
app.use(helmet());

app.use('/getStaticMap', require('./routes/getStaticMap'))

const port = process.env.PORT || 5001;

app.listen(port, () => {
    console.log(`app listening at http://localhost:${port}`);
  });
  