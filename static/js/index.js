let map, infoWindow;

// create a function to initiate the map
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        //set the initial location on the map.
        center: { lat: 53.3498, lng: -6.2603 },
        zoom: 14,
    });
    infoWindow = new google.maps.InfoWindow();

    // This part is to pan to the current location of user
    // https://developers.google.com/maps/documentation/javascript/geolocation
    const locationButton = document.createElement("button");

    locationButton.textContent = "Pan to Current Location";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
    locationButton.addEventListener("click", () => {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude,
                    };

                    infoWindow.setPosition(pos);
                    infoWindow.setContent("Location found.");
                    infoWindow.open(map);
                    map.setCenter(pos);
                },
                () => {
                    handleLocationError(true, infoWindow, map.getCenter());
                }
            );
        } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
        }
    });

    //create two variables to store the stationInfo and bikeInfo
    var station_info = stationInfo;
    var bike_info = bikeInfo;

    //iterate the stationInfo and bikeInfo and extract the key information.
    //iterate stationInfo firstly to extract the information of location, station number and station name.
    for (var i=0; i < stationInfo.length; i++){
        var location = new google.maps.LatLng(station_info[i].Latitude,station_info[i].Longitude);
        var stationNumber = station_info[i].Number;
        var stationName = station_info[i].Address;

        //create another for loop, to extract the dynamic information
        //when the bike_stationNumber equals to the stationNumber, extract the info of status, available_bikes and available_bike_stands
        for (var j=0; j < bikeInfo.length; j++){
            var bike_stationNumber = bike_info[j].Number;
            if (bike_stationNumber == stationNumber) {
                var status = bike_info[i].Status;
                var available_bikes = bike_info[i].Available_bikes;
                var available_bike_stands = bike_info[i].Available_bike_stands;
            }
            //add marker on the map
            addMarker(map, stationName, location);
        }
    }

    //create a variable called 'pre_infoWindow'.
    var pre_infoWindow = false;

    //create a function allMarker to add the marked location on the map.
    function addMarker(map, stationName, location) {
        var marker = new google.maps.Marker({
            position: location,
            title: stationName,
            map: map
        });

        //create a infoWindow to display the station info when clicking the location on the map
        var infoWindow = new google.maps.InfoWindow({
            content: '<h3>' + stationName + '</h3>' + '<p>' + 'Station Number: ' + stationNumber + '</p>' + '<p>' + 'Status: ' + status + '</p>' + '<p>' + 'Available bikes: ' + available_bikes + '</p>' + '<p>' + 'Available bike stands: ' + available_bike_stands + '</p>'
        })
        google.maps.event.addListener(marker, 'click', function (){
            if (pre_infoWindow) {
                pre_infoWindow.close();
            }
            pre_infoWindow = infoWindow
            infoWindow.open(map,marker);
        })
    }
}

//error handle
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation."
    );
    infoWindow.open(map);
}



