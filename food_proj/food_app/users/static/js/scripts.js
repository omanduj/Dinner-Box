$("form[name=login_form]").submit(function(e){     //when form=X, on submit, do this

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/token/login/", //this refers to url in flask layer to properly connect
        type: "POST",        //Type of operation
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);          //Used to show info on html inspect window
            var txt2 = $("<h2></h2>").text(Object.keys(resp));
            $('#token_title').html(txt2);
            $('#token_value').html(Object.values(resp));
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass('error--hidden');       //if error, will show text that is found in return statement
                                                    //of signup class. So it will print out the error whose key is error
        }
    })
    e.preventDefault();
});
