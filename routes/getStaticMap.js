const express = require("express");
const fs = require("fs");
const { PythonShell } = require("python-shell");
const path = require("path");
const router = new express.Router();
const Icon = require("../helpers/iconFactory");
require("dotenv").config();


router.post("/", async (req, res) => {
  // key is set in a .env file
  let key = req.body.key;

  if (key) {
    if (key == process.env.key) {
      try {
        console.log("wow");
        console.log(req.body);

        let staticIcons = req.body.staticIcons;
        let staticIconsList = "";

        let icons = req.body.icons || null;
        let iconsList = "";

        let markers = req.body.markers || null;
        let markersList = "";

        let center = req.body.center || null;
        let centerCoords = "";

        let lines = req.body.lines;
        let linesCoords = "";

        let polygons = req.body.polygons;
        let polygonCoords = "";

        if (icons) {
          iconsList = JSON.stringify(icons)
          icons.forEach(async (icon) => {
            console.log(icon);
            await Icon.make(icon.size, icon.tint, icon.symbol);
          });
        }
        console.log(staticIconsList)

        if (markers) {
          markersList = JSON.stringify(markers)
        }

        if (staticIcons) {
          staticIconsList = JSON.stringify(staticIcons)
        }

        if (center) {
          centerCoords = JSON.stringify(center)
        }

        if (lines) {
          linesCoords = JSON.stringify(lines)
        }

        if (polygons) {
          polygonCoords = JSON.stringify(polygons)
        }


        let options = {
          mode: "text",
          pythonPath: "/usr/bin/python3",
          pythonOptions: ["-u"], // get print results in real-time
          scriptPath: __dirname + "/../helpers/",
          args: [
            req.body.baseLayer || "topo",
            centerCoords || "None",
            req.body.zoom || "10",
            req.body.size || "400,400",
            iconsList || "None",
            markersList || "None",
            staticIconsList || "None",
            linesCoords || "None",
            polygonCoords || "None",
            req.body.customBaseURL || "None"
          ],
        };

        console.log(options["args"]);

        PythonShell.run("makeStaticMaps.py", options, function (err, results) {
          if (err) throw err;
          // results is an array consisting of messages collected during execution
          let fileName = results[0];
          console.log("results: %j", results);
          var options = {
            root: path.join(__dirname, "../public"),
            dotfiles: "deny",
            headers: {
              "x-timestamp": Date.now(),
              "x-sent": true,
            },
          };
          res.status(200).json({ filepath: encodeURI(`${req.protocol}://${req.get('host')}/${fileName}`)})
        });
      } catch (error) {
        console.log(error);
        res.status(500).json(error);
      }
    } else {
      res.status(403).json({ error: "invalid API key" });
    }
  } else {
    res.status(403).json({ error: "missing API key" });
  }
});

module.exports = router;

