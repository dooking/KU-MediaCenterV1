function init() {
  const htmllistDevice = document.getElementById("htmllist");
  const equipmentList = document.getElementById("equipmentList");

  if (equipmentList.value.includes("@@")) {
    const newlistsDevice = equipmentList.value.split("@@");
    for (let newlistDevice of newlistsDevice) {
      let item = document.createElement("p");
      const itemAttr = newlistDevice.split("^").join(" ");
      item.innerText = itemAttr;
      htmllistDevice.appendChild(item);
    }
  } else {
    const newlistsDevice = equipmentList.value
      .slice(1, -1)
      .replace(/'/g, "")
      .replace(/ /g, "")
      .split(",");
    for (let newlistDevice of newlistsDevice) {
      let item = document.createElement("p");

      const itemAttr = newlistDevice.split(":");
      item.innerText = itemAttr[0] + "    " + itemAttr[1] + "개";
      htmllistDevice.appendChild(item);
    }
  }
}

init();
