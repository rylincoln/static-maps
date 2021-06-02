const makizushi = require("@mapbox/makizushi");
const fs = require('fs')

const make = async (size, tint, symbol) => {
    makizushi({
        base: 'pin',
        size: size,
        tint: tint,
        symbol: symbol,
        retina: false
    }, function(err, buf) {
        if (err) throw err;
        fs.writeFileSync(__dirname + `/../icons/${symbol}.png`, buf);
    });
}
module.exports = { make };