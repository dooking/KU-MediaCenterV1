const fromTime = document.querySelector("#fromTime")
const toTime = document.querySelector("#toTime")
const toDate = document.querySelector("#toDate")
const fromDate = document.querySelector("#fromDate")
const selectDate = document.querySelector("#selectDate")

// 장비가 남아있는지 확인
let equipmentName= document.getElementsByClassName("equipmentName")
let equipmentCount= document.getElementsByClassName("equipmentCount")
let equipmentCount2= document.getElementsByClassName("equipmentCount2")
let checkCount = new Map()

for(let i=0; i<equipmentName.length; i++){
    let todayCount = equipmentCount[i].value.replace(/\[|\]/gi,"").split(",")
    let tomorrowCount = equipmentCount2[i].value.replace(/\[|\]/gi,"").split(",")
    checkCount.set(equipmentName[i].value,todayCount.concat(tomorrowCount))
}

let prevTime;
let nextTime;
let tempList = new Map()
selectDate.addEventListener('change',(event)=>{
    document.sDate.submit()
})

//예약 시간관리
fromTime.addEventListener('change',(event)=>{
    let sTime = (event.target.value).split(":")
    event.target.value=`${sTime[0]}:00`
    if(parseInt(sTime[0]) < 9 || parseInt(sTime[0]) > 17){
        alert("예약 시간은 오전 9시부터 오후 5시까지입니다.")
        event.target.value=`09:00`
    }
    prevTime = parseInt(sTime[0])
})
//반납 시간관리
toTime.addEventListener('change',(event)=>{
    let sTime = (event.target.value).split(":")
    event.target.value=`${sTime[0]}:00`
    nextTime = parseInt(sTime[0])
    if(parseInt(sTime[0]) < 9 || parseInt(sTime[0]) > 17){
        alert("반납 시간은 오전 9시부터 오후 5시까지입니다.")
        event.target.value=`17:00`
    }
    if(toDate.value === fromDate.value && prevTime > nextTime){
        alert("반납 시간이 대여 시간보다 빠릅니다.")
        event.target.value="17:00"
    }
})

function hide(thisisclicked) {
    // const className = "red_menu_text"
    // if(thisisclicked.nextElementSibling.classList[0]){
    //     thisisclicked.innerHTML = 
    //     `<p class=${className}>카메라</p>`+
    //     `<p class=${className}>▼</p>`;
    // }
    // else{
    //     thisisclicked.innerHTML = 
    //     `<p class=${className}>카메라</p>`+
    //     `<p class=${className}>▲</p>`;
    // }
    const hide = thisisclicked.nextElementSibling;
    hide.classList.toggle("mystyle");
}
function radioHandler(cb){
    const borrowList = document.querySelectorAll("li")
    const borrowClass = document.querySelector(".borrow_list")
    const addItem = document.createElement('li')
    let check = false
    let index = 0

    for(let i=0; i<borrowList.length; i++){
        if(borrowList[i].className === "camera"){
            check = true
            index = i
            break;
        }
    }
    if(check){
        borrowList[index].textContent = cb.value +" "+" 1개"
        tempList.set(cb.id,cb.value)
    }
    else{
        addItem.setAttribute("class","camera")
        addItem.textContent = cb.value +" "+"1개"
        borrowClass.appendChild(addItem)
        tempList.set(cb.id,cb.value)
    }
}
function checkHandler(cb){
    const borrowList = document.querySelectorAll("li")
    const borrowClass = document.querySelector(".borrow_list")
    const addItem = document.createElement('li')
    let check = false
    let index = 0
    for(let i=0; i<borrowList.length; i++){
        if(borrowList[i].className === `${cb.id}`){
            check = true
            index = i
            break;
        }
    }
    if(check){
        borrowClass.removeChild(borrowList[index])
        tempList.delete(cb.value)
    }
    else{
        addItem.setAttribute("class",`${cb.id}`)
        addItem.textContent = cb.value +" "+"1개"
        borrowClass.appendChild(addItem)
        tempList.set(cb.value,"1")
    }
}
function numberHandler(cb){
    const borrowClass = document.querySelector(".borrow_list")
    const borrowList = document.querySelectorAll("li")
    const addItem = document.createElement('li')
    let check = false
    let index = 0
    for(let i=0; i<borrowList.length; i++){
        if(borrowList[i].className === `${cb.id}`){
            check = true
            index = i
            break;
        }
    }
    // 해당 값이 0일 때
    if(cb.value == 0){
        cb.previousElementSibling.previousElementSibling.checked = false
        borrowClass.removeChild(borrowList[index])
        tempList.delete(cb.id)
        document.getElementById("etc").checked = false
    }
    else{
        // 해당 값이 이미 있을 때
        if(check){
            borrowList[index].textContent = cb.id +" "+cb.value +"개"
            tempList.set(cb.id,cb.value)
        }
        else{
            cb.previousElementSibling.previousElementSibling.checked = true
            addItem.setAttribute("class",`${cb.id}`)
            addItem.textContent = cb.id +" "+cb.value +"개"
            borrowClass.appendChild(addItem)
            tempList.set(cb.id,cb.value)
        }
    }
}

function checkAll(){
    const resultBorrow = document.getElementById("resultBorrow")
    let resultBorrowString = ""
    let isCamera = false
    if(tempList.size === 0){
        alert("대여 장비 목록이 존재하지 않습니다")
        return false
    }
    for(let [key,value] of tempList.entries()){
        if(key==="camera"){
            resultBorrowString += value +" : "+"1"+"//"
            isCamera = true
        }
        else{
            resultBorrowString += key +" : "+value+"//"
            isCamera = false
        }
        // 재고가 있는지 확인 (당일 반납 + 내일 반납)
        if(!checkStock(key,value,isCamera)){
            alert(`${key}의 재고가 존재하지 않습니다`)
            return false
        }
    }
    resultBorrow.value = resultBorrowString
    return true
}

function checkStock(key,value,isCamera){
    const checkstock = isCamera ? checkCount.get(value) : checkCount.get(key)
    let FromTime = parseInt((fromTime.value).split(":")[0])
    let ToTime = parseInt((toTime.value).split(":")[0])
    let check = true
    if(fromDate.value == toDate.value){
        checkstock.slice(FromTime-9,ToTime-8).some(v=>{
            const isMinus = isCamera ? v-1 : v-value
            if(isMinus < 0){
                check = false
            }
        })
    }
    else{
        checkstock.slice(FromTime-9,ToTime+1).some(v=>{
            const isMinus = isCamera ? v-1 : v-value
            if(isMinus < 0){
                check = false
            }
        })
    }
    return check
}
//time block
for (let index=0; index<18; index++){
    let blockCount = document.getElementsByClassName(String(index))
    for (let i=0; i<blockCount.length; i++)
    {
        for (let j=0; j<blockCount[i].id; j++){
            const newDiv = document.createElement('div')
            newDiv.setAttribute("class","time-block")
            blockCount[i].appendChild(newDiv);
        }
    }
}