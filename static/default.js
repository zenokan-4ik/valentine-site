function get_profile() {
    $.post('/get_name', function(data){profile_name.innerText = data})
}

function display_elem() {
    if(isExit){
        profile_menu.style.display = "none";
        isExit = false;
    }
    else{
        profile_menu.style.display = "flex";
        isExit = true;
    }
}

function logout(){
    $.post("/logout", function(response){get_profile()})
}

function to_linktree() {
    window.location.href = '/';
}

function clear_textareas_reg() {
    name_text.value = '';
    email_text.value = '';
    login_text.value = '';
    password_text.value = '';
}

function clear_textareas_login() {
    login_text.value = '';
    password_text.value = '';
}

function confirm_login() {
    $.get("/login", {
        login: login_text.value,
        password: password_text.value
    }, function(data) {
        success_text.innerText = data;
        get_profile();
        clear_textareas_login();
    });
}

function confirm_reg() {
    $.get("/register", {
        name: name_text.value,
        login: login_text.value,
        password: password_text.value,
        email: email_text.value
    }, function(data) {
        success_text.innerText = data;
        if(data=='Успешно!'){get_profile()};
        clear_textareas_reg();
    });
}

function to_profile() {
    window.location.href = '/profile';
}

function edit_profile() {
    console.log('qwe');
    $.get('/profile/edit', {
        login: new_login.value,
        name: new_name.value,
        email: new_email.value,
        password: new_password.value
    }, function(response){
        changed_data_text.innerText = response;
    })
}

function show_editing() {
    if(isEdit){
        new_data.style.display = "none";
        isEdit = false;
    }
    else{
        new_data.style.display = "flex";
        isEdit = true;
    }
}