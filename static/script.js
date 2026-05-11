class Crater {
    name = ''; //string
    country = ''; //string
    latitude = 0.0; //float
    longitude = 0.0; //float
    diameter = 0.0; //float
    age = 0.0;
    ageDeviation = 0.0;

    element;
    mapMarker;
}

var craterList = [];

var craterMinMax = [0, 0];

var map;
var markerLayer;

function getCraterName(item) {
   return item.querySelector('button').innerText;
}

function getCraterCountry(item) {
    return item.querySelector('div > ul > li').innerText;
}

function coordsParse(text) {
   text = text.replace(/\D|'/, " ");
   text = text.replace("'", " ");

   let split = text.split("°");

   let res = parseFloat(split[1]);
//document.write(split[1])
   res = res / 60;
   res = res + parseFloat(split[0]);
   return res;
}
   
   

function getCraterLatitude(item) {
    let text = item.querySelector('div > ul > li + li').innerText.toLowerCase();
    let split = text.split(": ");
    return coordsParse(split[1]);
}

function getCraterLongitude(item) {
    let text = item.querySelector('div > ul > li + li + li').innerText.toLowerCase();
    let split = text.split(": ");
    return coordsParse(split[1]);
}

function getCraterDiam(item) {
    let text = item.querySelector('div > ul > li + li + li + li').innerText.toLowerCase();
    let split = text.split(": ");
    let num = split[1].replace(/\D/, " ");
    return parseFloat(num);
}

function getCraterAge(item) {
    let text = item.querySelector('div > ul > li + li + li + li + li').innerText.toLowerCase();
    let split1 = text.split(": ");
    if(split1[1].includes("±")) {
	let num = split1[1].split("±")[0].replace(/\D/, " ");;
    	return parseFloat(num);
    } else {
	let num = split1[1].replace(/\D/, " ");
    	return parseFloat(num);
//return 12;
    }
}

function getCraterAgeDeviation(item) {
    let text = item.querySelector('div > ul > li + li + li + li + li').innerText.toLowerCase();
    let split1 = text.split(": ");
    if(split1[1].includes("±")) {
	let split2 = split1[1].split("±");
    	return parseFloat(split2[1]);
    } else {
	return 1;
    }
}

function initializeCraters() {
    let items = document.querySelectorAll('.crater-item');

   items.forEach(item => {
        var newCrater = new Crater();

        newCrater.name = getCraterName(item);
        newCrater.country = getCraterCountry(item);
        newCrater.latitude = getCraterLatitude(item);
        newCrater.longitude = getCraterLongitude(item);
        newCrater.diameter = getCraterDiam(item);
        newCrater.age = getCraterAge(item);
        newCrater.ageDeviation = getCraterAgeDeviation(item);

        newCrater.element = item;

	craterMinMax[0] = Math.min(craterMinMax[0], newCrater.diameter);
	craterMinMax[1] = Math.max(craterMinMax[1], newCrater.diameter);

	//console.log([newCrater.name, newCrater.age, newCrater.ageDeviation]);

        //Makes buttons do stuff when clicked
        let button = item.querySelector('button');
        button.addEventListener("click", () => {
            //Showing crater details
            const details = button.nextElementSibling;
            const shownStyle = "flex";

            details.style.display = (details.style.display === "none") ? shownStyle : "none";

            //Popup for marker
            if (newCrater.mapMarker != null) {
                if (details.style.display === shownStyle) {
                    newCrater.mapMarker.openPopup();
                } else {
                    newCrater.mapMarker.closePopup();
                }
            }

        });

        craterList.push(newCrater);
    });
}

function generateCraterMarkers() {
    //Put craters on map
    craterRange = craterMinMax[1] - craterMinMax[0];
    craterList.forEach(crater => {
	let scale = Math.max(crater.diameter, 1) / craterRange + 0.5;
	//scale = Math.log(scale) / 3;
//Defaults are iconSize: [25, 41], shadowSize:  [41, 41]; from source code
        let icon = new L.Icon.Default({iconSize: [25, 41].map((x) => x * scale), 
				       shadowSize:  [41, 41].map((x) => x * scale)});
        let marker = L.marker([crater.latitude, crater.longitude], {icon: icon});
        marker.addTo(markerLayer).bindPopup(crater.name); //.openPopup();
        crater.mapMarker = marker;
    });

   markerLayer.addTo(map);

}

window.onload = (event) => {
    initializeCraters();
    generateCraterMarkers();
};

// 🔍 Vyhledávání
function filterCraters() {
    //Loads fields
    let name = document.getElementById('search').value.toLowerCase() ?? "";
    let country = document.getElementById('searchCountry').value.toLowerCase() ?? "";

    let minDiam = document.getElementById('minDiameter').value ?? 0;
    let maxDiam = document.getElementById('maxDiameter').value || 9999;

    let minAge = document.getElementById('minAge').value ?? 0;
    let maxAge = document.getElementById('maxAge').value || 9999;



    console.log(maxAge);

    let items = document.querySelectorAll('.crater-item');

    //Filters the craters
    craterList.forEach(crater => {
        let craterName = crater.name.toLowerCase(); //item.querySelector('button').innerText.toLowerCase();
        let correctName = craterName.includes(name);

        let craterCountry = crater.country.toLowerCase();
        let correctCountry = craterCountry.includes(country);

        let diam = crater.diameter;
        let correctDiam = (minDiam <= diam && diam <= maxDiam);

        let age = crater.age;
        let ageDeviation = crater.ageDeviation;
        let correctAge = (minAge <= (age + ageDeviation)
                            && (age - ageDeviation) <= maxAge);

        let craterMatches = (correctName && correctCountry && correctDiam && correctAge);

        crater.element.style.display = craterMatches ? '' : 'none';

        if (craterMatches) {
            crater.mapMarker.addTo(map);
        } else {
            crater.mapMarker.remove();
        }

    });
}

// 🗺️ ZOBRAZENÍ MAPY S KRÁTERY
document.addEventListener("DOMContentLoaded", () => {
  // Inicializace mapy
  map = L.map("map").setView([60.1, 20.1], 2.5); // [lat, lng], zoom
  markerLayer = L.layerGroup();

  // Přidání podkladové vrstvy
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

});

//Tmavý režim
document.addEventListener("DOMContentLoaded", () => {
    const switcher = document.getElementById("themeSwitch");
    const body = document.body;


    switcher.addEventListener("change", () => {
        body.classList.toggle("dark-mode");
    });
});


