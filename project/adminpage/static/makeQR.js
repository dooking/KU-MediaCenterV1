function makeCode(qrDiv) {
  const equipmentName = document.getElementById("equipmentName");
  const serialNumber = document.getElementById("serialNumber");
  const equipType = document.getElementById("equipType");
  const equipSemiType = document.getElementById("equipSemiType");

  if (
    !equipmentName.value ||
    !equipType.value ||
    !equipSemiType.value ||
    !serialNumber.value
  ) {
    alert("input을 모두 입력해주세요");
    equipmentName.focus();
    return;
  }
  const newEquipment = `${equipmentName.value}^${serialNumber.value}^${equipType.value}^${equipSemiType.value}`;

  new QRCode(qrDiv, {
    text: newEquipment,
    width: 100,
    height: 100,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.H,
  });
  //qrcode.makeCode(newEquipment);
}

const makeQRBtn = document.getElementById("makeQRcode");
const submitBtn = document.getElementById("submit_form");

makeQRBtn.addEventListener("click", () => {
  makeQRBtn.style.display = "none";
  const qrDiv = document.getElementById("qrcode");
  qrDiv.style.display = "block";
  makeCode(qrDiv);
  submitBtn.style.display = "block";
});
