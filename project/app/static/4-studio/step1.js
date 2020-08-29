const fromTime = document.querySelector("#fromTime")
const toTime = document.querySelector("#toTime")
const toDate = document.querySelector("#toDate")
const fromDate = document.querySelector("#fromDate")
const selectDate = document.querySelector("#selectDate")

// 장비가 남아있는지 확인
let studioName= document.getElementsByClassName("studioName")
let studioCount= document.getElementsByClassName("studioCount")
let studioCount2= document.getElementsByClassName("studioCount2")
let checkCount = new Map()

for(let i=0; i<studioName.length; i++){
    let todayCount = studioCount[i].value.replace(/\[|\]/gi,"").split(",")
    let tomorrowCount = studioCount2[i].value.replace(/\[|\]/gi,"").split(",")
    checkCount.set(studioName[i].value,todayCount.concat(tomorrowCount))
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
        alert("오전 9시부터 오후 5시 사이에 카드를 찾으셔야 합니다.")
    }
    prevTime = parseInt(sTime[0])
})
//반납 시간관리
toTime.addEventListener('change',(event)=>{
    let sTime = (event.target.value).split(":")
    event.target.value=`${sTime[0]}:00`
    nextTime = parseInt(sTime[0])
    if(parseInt(sTime[0]) < 9 || parseInt(sTime[0]) > 17){
        alert("오전 9시부터 오후 5시 사이에 카드를 찾으셔야 합니다.")
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
    const hide = thisisclicked.parentNode.nextElementSibling;
    hide.classList.toggle("mystyle");
}
function radioHandler(cb){
    const borrowList = document.querySelectorAll("li")
    const borrowClass = document.querySelector(".borrow_list")
    const addItem = document.createElement('li')
    let check = false
    let index = 0

    for(let i=0; i<borrowList.length; i++){
        if(borrowList[i].className === "edit"){
            check = true
            index = i
            break;
        }
    }
    if(check){
        borrowList[index].textContent = cb.value
        tempList.set(cb.value,"1")
    }
    else{
        addItem.setAttribute("class","edit")
        addItem.textContent = cb.value
        borrowClass.appendChild(addItem)
        tempList.set(cb.value,"1")
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
        addItem.textContent = cb.value
        borrowClass.appendChild(addItem)
        tempList.set(cb.value,"1")
    }
}
function checkAll(){
    const resultBorrow = document.getElementById("resultBorrow")
    let resultBorrowString = ""
    console.log(tempList)
    if(tempList.size === 0){
        alert("대여 장비 목록이 존재하지 않습니다")
        return false
    }
    for(let [key,value] of tempList.entries()){
        resultBorrowString += key +"//"
        // 재고가 있는지 확인 (당일 반납 + 내일 반납)
        if(!checkStock(key,value)){
            alert(`${key}의 예약이 존재합니다`)
            return false
        }
    }
    resultBorrow.value = resultBorrowString
    return true
}

function checkStock(key,value){
    const checkstock = checkCount.get(key)
    let FromTime = parseInt((fromTime.value).split(":")[0])
    let ToTime = parseInt((toTime.value).split(":")[0])
    let check = true
    if(fromDate.value == toDate.value){
        checkstock.slice(FromTime,ToTime).some(v=>{
            const isMinus = v-parseInt(value)
            if(isMinus < 0){
                check = false
            }
        })
    }
    else{
        checkstock.slice(FromTime,ToTime+23).some(v=>{
            const isMinus = v-value
            if(isMinus < 0){
                check = false
            }
        })
    }
    return check
}

//time block
for (let index=0; index<50; index++){
    let blockCount = document.getElementsByClassName(String(index))
    console.log("index :",index,blockCount.length)
    for (let i=0; i<blockCount.length; i++)
    {
        for (let j=0; j<blockCount[i].id; j++){
            const newDiv = document.createElement('div')
            newDiv.setAttribute("class","time-block")
            blockCount[i].appendChild(newDiv);
        }
    }
}