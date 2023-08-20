const defaultColors = [
    "#3366CC", "#DC3912", "#FF9900", "#109618", "#990099", "#3B3EAC"
];
const defaultGreys = [
    "rgba(100,100,100,1)", "rgba(125,125,125,1)", "rgba(150,150,150,1)",
    "rgba(175,175,175,1)", "rgba(200,200,200,1)", "rgba(225,225,225,1)"
];
const defaultLabels = [
    'Temperature/50', 'Humidity/100', 'Pressure/2000', 'Oxidised/100', 'Reduced/1000', 'NH3/400',
    'pm03/20000', 'pm05/1000', 'pm10/2000', 'pm25/500', 'pm50/200', 'pm100/100'
];
const normValues = {
    'temp': 50,
    'humi': 100,
    'pres': 2000,
    'oxi': 100,
    'red': 1000,
    'nh3': 400,
    'pm03': 20000,
    'pm05': 1000,
    'pm10': 2000,
    'pm25': 500,
    'pm50': 200,
    'pm100': 100
};
const formalDataTypes = {
    'temp': 'Temperature',
    'humi': 'Humidity',
    'pres': 'Pressure',
    'oxi': 'Oxidising',
    'red': 'Reducing',
    'nh3': 'NH<sub>3</sub>',
    'pm03': '>0.3um',
    'pm05': '>0.5um',
    'pm10': '>1.0um',
    'pm25': '>1.0um',
    'pm50': '>5.0um',
    'pm100': '>10.0um'
};
const dataUnits = {
    'temp': '&deg;C',
    'humi': '%',
    'pres': '&nbsp;mBar',
    'oxi': '&nbsp;k&Omega;',
    'red': '&nbsp;k&Omega;',
    'nh3': '&nbsp;k&Omega;',
    'pm03': '&nbsp;/&nbsp;0.1l',
    'pm05': '&nbsp;/&nbsp;0.1l',
    'pm10': '&nbsp;/&nbsp;0.1l',
    'pm25': '&nbsp;/&nbsp;0.1l',
    'pm50': '&nbsp;/&nbsp;0.1l',
    'pm100': '&nbsp;/&nbsp;0.1l'
};

async function fetchJsonDataArray() {
    try {
        const res = [];
        const response = await fetch('/get_data_files');
        const data = await response.json();
        const fileNames = data.files;

        for (const fileName of fileNames) {
            const response = await fetch(`/enviro-data/${fileName}`);
            const jsonData = await response.json();
            res.push(jsonData);
        }
        return res;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function displayLatestData(jsonDataArray) {
    const latestData = {};
    if (jsonDataArray.length > 0) {
        const latestDataPoint = jsonDataArray[jsonDataArray.length - 1];
        for (const key in latestDataPoint) {
            latestData[key] = latestDataPoint[key];
        }
    }

    let latestDataTable = document.getElementById("latest_data");
    let tableBody = document.createElement("tbody");
    for (const key in latestData) {
        const tableRow = document.createElement("tr");
        if (key == 'time') {
            const tableData = document.createElement("td");
            tableData.textContent = latestData[key];
            tableData.setAttribute("colspan", "2");
            tableRow.appendChild(tableData);
            tableBody.appendChild(tableRow);
            continue;
        }

        const tableData1 = document.createElement("td");
        tableData1.innerHTML = formalDataTypes[key] + ':';
        tableRow.appendChild(tableData1);

        const tableData2 = document.createElement("td");
        tableData2.innerHTML = latestData[key];
        tableData2.innerHTML += dataUnits[key];
        tableRow.appendChild(tableData2);

        tableBody.appendChild(tableRow);
    }
    latestDataTable.appendChild(tableBody);
}

async function createChart(jsonDataArray) {
    const ctx = document.getElementById('lineChart');

    const labels = jsonDataArray.map(data => data.time);

    const datasets = [];
    const dataKeys = Object.keys(jsonDataArray[0]).filter(key => key !== 'time');

    for (let i = 0; i < dataKeys.length; i++) {
        const key = dataKeys[i];
        const dataPoints = jsonDataArray.map(data => data[key] / normValues[key]);

        // color assignement
        let backgroundColor;
        if (i < 6) {
            backgroundColor = defaultColors[i];
        } else {
            const greyIndex = i - 6;
            backgroundColor = defaultGreys[greyIndex];
        }

        const dataset = {
            label: defaultLabels[i],
            data: dataPoints,
            fill: false,
            borderColor: backgroundColor,
            backgroundColor: backgroundColor,
        };
        datasets.push(dataset);
    }

    const cfg = {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets,
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            },
            plugins: {
                legend: {
                    position: 'bottom'
                }
            },
            reponsive: false
        }
    };

    new Chart(ctx, cfg);
}

document.addEventListener("DOMContentLoaded", async function () {
    const jsonDataArray = await fetchJsonDataArray();
    printData(jsonDataArray);
    displayLatestData(jsonDataArray);
    createChart(jsonDataArray);
});