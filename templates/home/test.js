// Function to get latitude and longitude from the browser's Geolocation API
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}

// Callback function to handle the user's location data
function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    console.log(`Latitude: ${lat}, Longitude: ${lon}`);
    
    // Now use the coordinates for reverse geocoding
    reverseGeocode(lat, lon);
}

// Function to reverse geocode (convert lat/lon into city/state/pincode)
function reverseGeocode(lat, lon) {
    const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`;

    fetch(url)
    .then(response => response.json())
    .then(data => {
        const city = data.address.city || data.address.town || data.address.village;
        const state = data.address.state;
        const pincode = data.address.postcode;
        console.log(`City: ${city}, State: ${state}, Pincode: ${pincode}`);
    })
    .catch(error => console.error('Error with reverse geocoding:', error));
}

// Function to handle errors in getting location
function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.error("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            console.error("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            console.error("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            console.error("An unknown error occurred.");
            break;
    }
}

// Call the function to get the user's location
getLocation();
