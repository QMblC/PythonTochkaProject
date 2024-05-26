function renderAddresses(addresses) {
  const addressList = document.querySelector(".addresses");
  const p = document.createElement("p");
  p.textContent = "Адреса"
  const ul = document.createElement("ul");

  addresses.forEach((address) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = "addresses/" + address[0] + "/";
    a.textContent = address[1];
    li.append(a);
    ul.append(li);
  });
  addressList.append(p);
  addressList.append(ul);
}


function fetchAddresses() {
  fetch("/api/getaddresses/")
    .then((response) => response.json())
    .then((data) => renderAddresses(data));
}

fetchAddresses();