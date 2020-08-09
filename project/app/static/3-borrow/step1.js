function hide(thisisclicked) {
    const hide = thisisclicked.nextElementSibling;
    hide.classList.toggle("mystyle");
    }
function radioHandler(cb){
    const check = document.querySelector(".hihi")
    if(check == null){
        const here = document.querySelector(".here")
        const newDiv = document.createElement('div')
        newDiv.setAttribute("class","hihi")
        newDiv.textContent = cb.value
        here.appendChild(newDiv);
    }
    else{
        console.log(check)
        check.textContent = cb.value
    }
}
function checkHandler(cb){
    if(cb.checked){

    }
    else{
        const here = document.querySelector(".here")
        const newDiv = document.createElement('div')
        newDiv.setAttribute("class","hihi")
        newDiv.textContent = cb.value
        here.appendChild(newDiv);
    }
}
function dataHandler(cb){
    cb.preventDefault();
}
function sliderHandler(cb){
    const check = document.querySelector(".hiz")
    if(check == null){
        const here = document.querySelector(".here")
        const newDiv = document.createElement('div')
        newDiv.setAttribute("class","hiz")
        newDiv.textContent = cb.id + " "+cb.value+"개"
        here.appendChild(newDiv);
    }
    else{
        console.log(check)
        check.textContent = cb.id + " "+cb.value+"개"
    }
}
function memoryHandler(cb){
    const check = document.querySelector(".hi")
    if(check == null){
        const here = document.querySelector(".here")
        const newDiv = document.createElement('div')
        newDiv.setAttribute("class","hi")
        newDiv.textContent = cb.id + " "+cb.value+"개"
        here.appendChild(newDiv);
    }
    else{
        console.log(check)
        check.textContent = cb.id + " "+cb.value+"개"
    }
}