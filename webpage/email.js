// Function to remove row and update the server
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

  // delete DOM element
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

function addEmailRow(address, types) {
  // create DOM elements
  const row = document.createElement("tr")
  const email = document.createElement("td")
  const typesCell = document.createElement("td")
  const iconCell = document.createElement("td")
  const icon = document.createElement('i')
  icon.setAttribute('class', 'bx bx-trash')

  // Set email address
  email.innerHTML = `${address}`

  // get notification types in display format
  let fulltypes = []
  if (charInString("l", types)) fulltypes.push("Light")
  if (charInString("t", types)) fulltypes.push("Temperature")
  if (charInString("h", types)) fulltypes.push("Humidity")
  typesCell.innerHTML = fulltypes.join(", ")

  // Add nodes in correct structure
  row.appendChild(email)
  row.appendChild(typesCell)
  row.appendChild(iconCell)
  document.querySelector(".email-list").appendChild(row)

  // put icon inside of iconCell
  iconCell.appendChild(icon);

  // activate remove button icon
  icon.addEventListener("click", () => removeRow(icon))
}

function showOverlay() {
  document.querySelector('.overlay').style.display = 'block'
}

function hideOverlay() {
  document.querySelector('.overlay').style.display = 'none'
}

function validateEmail(email) {
  const re = /\S+@\S+\.\S+/;
  return re.test(email);
}

// Structure:
// emails = {
//   'nboxer@usc.edu': 'lth',
//   'jackblackadar@icloud.com': 'lt'
// }

// load emails from server
fetch(`${SERVER}/email`)
  .then((response) => response.json())
  .then((emails) => {
    for (const address in emails) {
      addEmailRow(address, emails[address])
    }
  })
  .catch(err => console.log(err))

// Add email address button - shows popup.
const addEmail = document.querySelector(".add-email-address")
addEmail.addEventListener("click", () => showOverlay())

// close-email-popup-button - closes "add email" popup
const closePopup = document.getElementById('close-email-popup-button')
closePopup.addEventListener("click", () => hideOverlay())

// confirm add email address - button on popup that when clicked,
// adds an email with new notifications.
const confirmAddEmail = document.getElementById('confirm-add-email');
confirmAddEmail.addEventListener('click', () => {
  
  const email = document.getElementById('email-input').value
  
  let types = ""
  if (document.getElementById('light-alert-checkbox').checked) types += 'l'
  if (document.getElementById('temp-alert-checkbox').checked) types += 't'
  if (document.getElementById('humid-alert-checkbox').checked) types += 'h'

  // validate inputs
  if (validateEmail(email) && types !== "") {
    // send POST to server
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      'body': JSON.stringify({
        'email': email,
        'types': types
      })
    }

    fetch('/email', options)
      .then(response => {
        addEmailRow(email, types)
      })
    
    hideOverlay()
  }
  else {
    alert('Please enter a valid email address and check at least one box')
  }
  
})