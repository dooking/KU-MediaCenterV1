const fromTime = document.querySelector("#fromTime")
const toTime = document.querySelector("#toTime")
const toDate = document.querySelector("#toDate")
const fromDate = document.querySelector("#fromDate")
let prevTime;
let nextTime;
let tempList = new Map()
fromTime.addEventListener('change',(event)=>{
    let sTime = (event.target.value).split(":")
    event.target.value=`${sTime[0]}:00`
    if(parseInt(sTime[0]) < 9 || parseInt(sTime[0]) > 17){
        alert("예약 시간은 오전 9시부터 오후 5시까지입니다.")
        event.target.value=`09:00`
    }
    prevTime = parseInt(sTime[0])
})
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
function numberHandler(cb){
    if(cb.value != ""){
        if(cb.value > 5){
            alert("장비는 최대 5개까지 대여가 가능합니다.")
            cb.value = 5
        }
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
        if(cb.value == 0){
            borrowClass.removeChild(borrowList[index])
            tempList.delete(cb.id)
        }
        else{
            // 해당 값이 이미 있을 때
            if(check){
                borrowList[index].textContent = cb.id +" "+cb.value +"개"
                tempList.set(cb.id,cb.value)
            }
            else{
                addItem.setAttribute("class",`${cb.id}`)
                addItem.textContent = cb.id +" "+cb.value +"개"
                borrowClass.appendChild(addItem)
                tempList.set(cb.id,cb.value)
            }
        }
    }
}

function buttonHandler(cb){
    const resultBorrow = document.getElementById("resultBorrow")
    let resultBorrowString = ""
    for(let [key,value] of tempList.entries()){
        if(key == "camera"){
            resultBorrowString += value +" : "+1+"//"
        }
        else{
            resultBorrowString += key +" : "+value+"//"
        }
    }
    resultBorrow.value = resultBorrowString
    document.step1.submit()
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