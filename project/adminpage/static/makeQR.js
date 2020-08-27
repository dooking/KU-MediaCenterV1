function makeCode() {
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

  new QRCode(document.getElementById("qrcode"), {
    text: newEquipment,
    width: 100,
    height: 100,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.H,
  });
  //qrcode.makeCode(newEquipment);
}
