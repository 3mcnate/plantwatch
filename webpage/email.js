function removeRow(icon) {
  const row = icon.parentNode.parentNode
  const email = row.childNodes[0].innerHTML

  // delete email from server
  options = {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
    }),
  }

  // send HTTP request to delete email
  fetch(`${SERVER}/email`, options)
    .then((response) => {
      if (response.ok) {
        console.log("successfully deleted email")
      }
    })
    .catch((err) => console.log(err))

  row.remove()
}

function charInString(char, str) {
  for (let i = 0; i < str.length; i++) {
    if (char == str[i]) {
      return true
    }
  }
  return false
}

// load emails from server
fetch(`${SERVER}/email`)
  .then((response) => response.json())
  .then((emails) => {
    for (const address in emails) {
      const row = document.createElement("tr")
      const email = document.createElement("td")
      const types = document.createElement("td")
      const icon = document.createElement("td")

      email.innerHTML = `${address}`

      let fulltypes = []
      if (charInString("l", emails[address])) fulltypes.push("Light")
      if (charInString("t", emails[address])) fulltypes.push("Temperature")
      if (charInString("h", emails[address])) fulltypes.push("Humidity")
      types.innerHTML = fulltypes.join(", ")

      icon.innerHTML = `<i class='bx bx-trash'></i>`

      row.appendChild(email)
      row.appendChild(types)
      row.appendChild(icon)
      document.querySelector(".email-list").appendChild(row)

      // activate remove buttons
      document.querySelectorAll("td i").forEach((icon) => {
        icon.addEventListener("click", () => removeRow(icon))
      })
    }
  })
