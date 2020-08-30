let tempList = new Map()

function hide(thisisclicked) {
    const hide = thisisclicked.nextElementSibling;
    hide.classList.toggle("mystyle");
}


function radioHandler(cb){
    const borrowList = document.querySelectorAll("li")
    const borrowClass = document.querySelector(".borrow_list")
    const addItem = document.createElement('li')
    let check = false
    let index = 0
    console.log(cb.id,cb.value)

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