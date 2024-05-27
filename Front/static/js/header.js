async function function1() {
    var ul = document.getElementById("header");
    var li = document.createElement("li");

    if (!document.cookie.includes("jwt")) {
        
        li.innerHTML = `<a href="/login/">Вход</a>`;
        ul.appendChild(li);
    }
    else{
        li.innerHTML = `
        <a href="javascript:logout();">Выйти</a>
        `;
        ul.appendChild(li);
    }
}

function logout(){
    let newCookie = "";
    let split = document.cookie.split(';');
    for(var i = 0; i < split.length; i++){
        console.log(newCookie);
        if (split[i].includes("jwt=")){
            newCookie += split[i] + ";max-age=-1;";
        }
        else{
            newCookie += split[i];
        }
    }
    document.cookie = newCookie;
    console.log(document.cookie);

    location.reload()
}