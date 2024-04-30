const SERVER = "http://127.0.0.1:5000"

function getData() {
  fetch(`${SERVER}/sensor`)
    .then((response) => response.json())
    .then((data) => updateData(data))
}

function updateData(data) {
  const light = document.getElementById("light-value")
  const temp = document.getElementById("temp-value")
  const humidity = document.getElementById("humidity-value")

  light.innerHTML = data[0]
  humidity.innerHTML = data[1]
  temp.innerHTML = data[2]

  setTimeout(getData, 1000)
}

getData()

