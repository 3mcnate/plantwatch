function isNumeric(str) {
  if (typeof str != "string") return false // we only process strings!
  return (
    !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
    !isNaN(parseFloat(str))
  ) // ...and ensure strings of whitespace fail
}

function onBlurThreshold(val, inputField) {
  console.log("triggered")
  // remove input field
  inputField.style.display = "none"
  const oldVal = val.innerHTML.split(" ")[0]

  if (
    isNumeric(inputField.value) &&
    inputField.value >= 0 &&
    inputField.value <= 1000
  ) {
    // constuct HTTP request
    options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        threshold: val.id,
        value: inputField.value,
      }),
    }

    // send HTTP request to update threshold values
    fetch(`${SERVER}/threshold`, options)
      .then((response) => {
        if (response.ok) {
          console.log("successfully updated threshold value")
        }
      })
      .catch((err) => console.log(err))

    // update the threshold value to the user, only if valid
    val.innerHTML = `${inputField.value} <i class='bx bx-edit-alt'></i>`
  }
  else {
    inputField.value = oldVal
    inputField.style.border = "1px solid red"
  }

  // show the threshold value again
  val.style.display = "block"
}

// set input field event for all threshold values
document.querySelectorAll(".threshold-value").forEach((val) => {
  const inputField = val.nextElementSibling
  val.addEventListener("click", () => {
    val.style.display = "none"
    inputField.style.display = "block"
    inputField.focus()
  })

  // add event listener for losing focus
  inputField.addEventListener("blur", () => onBlurThreshold(val, inputField))
  inputField.addEventListener("keypress", (e) => {
    if (e.key == "Enter") {
      inputField.blur()
    }
  })
  inputField.value = val.innerHTML.split(" ")[0]
})

// event listeners
const threshold_id_list = ["light-low", "light-high", "temp-low", "temp-high", "humid-low", "humid-high"]

fetch(`${SERVER}/thresholds`)
  .then(response => response.json())
  .then(thresholds => {
    for (let i = 0; i < 6; i++) {
      document.getElementById(threshold_id_list[i])
              .innerHTML = `${thresholds[threshold_id_list[i]]} <i class='bx bx-edit-alt'></i>`;
    }
  })

