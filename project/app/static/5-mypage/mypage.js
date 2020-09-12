const openEquipModal = function (btnID) {
    try {
        const ID = btnID.slice(-1)
        const modalID = `Equip_modal_${ID}`

        const modal = document.getElementById(`${modalID}`)
        const borrowState = modal.querySelector(`#borrowState_${ID}`).value

        if (borrowState != 0) {
            throw new Error("대여 중에는 예약 취소가 불가능합니다.")
        }

        modal.classList.remove('modal_close')
        modal.classList.add('modal_open')
    } catch (e) {
        alert(e.message)
    }
}

const openStudioModal = function (btnID) {
    try {
        const ID = btnID.slice(-1)
        const modalID = `Studio_modal_${ID}`

        const modal = document.getElementById(`${modalID}`)
        const studioState = modal.querySelector(`#studioState_${ID}`).value

        if (studioState != 0) {
            throw new Error("대여 중에는 예약 취소가 불가능합니다.")
        }
        modal.classList.remove('modal_close')
        modal.classList.add('modal_open')
    } catch (e) {
        alert(e.message)
    }
}
