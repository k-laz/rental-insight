import vancouverNeighborhoods from "./vancouver_neighborhoods.js";

var map = L.map("mapid").setView([49.2827, -123.1207], 12); // Center on Vancouver

// L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//   maxZoom: 18,
// }).addTo(map);

// Assuming your GeoJSON data is stored in a variable named vancouverNeighborhoods
L.geoJSON(vancouverNeighborhoods, {
  onEachFeature: function (feature, layer) {
    // Example: Add a popup or any other interaction
    layer.bindPopup(feature.properties.name); // Assuming 'name' is a property of each feature

    // Add click event
    layer.on("click", function () {
      // Example: toggle a checkbox status, update UI, etc.
      console.log(`Clicked on ${feature.properties.name}`);
      // Implement functionality as needed, e.g., toggle checkboxes
    });
  },
}).addTo(map);
