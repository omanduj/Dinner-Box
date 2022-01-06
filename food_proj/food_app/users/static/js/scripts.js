$("form[name=login_form]").submit(function(e){     //when form=X, on submit, do this

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/token/login/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            var txt2 = $("<h2></h2>").text(Object.keys(resp));
            $('#token_title').html(txt2);
            $('#token_value').html(Object.values(resp));
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass('error--hidden');
        }
    })
    e.preventDefault();
});

$("form[name=find_food]").submit(function(e){     //when form=X, on submit, do this

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/foodpicker",
        type: "POST",        //Type of operation
        data: data,
        dataType: "json",
        success: function(resp) {
            var name = 'Name: ' + resp['You have been Registered']['Restaurant Name']
            var rating = 'Rating: ' + resp['You have been Registered']['Rating']
            var price = 'Price: ' + resp['You have been Registered']['Price']

            if (resp['You have been Registered']['Location']) {
                var location = 'Location: ' + resp['You have been Registered']['Location']
            }  else {
                var location = 'Location: N/a'
            }

            var genre = 'Genre: '

            for (const [key, value] of Object.entries(resp['You have been Registered']['Genre'])) {
                genre += value['title'] + ', '
            }

            $('#name').html(name);
            $('#rating').html(rating);
            $('#price').html(price);
            $('#location').html(location);
            $('#genre').html(genre.slice(0, genre.length - 2));
        },
        error: function(resp) {
            console.log(resp);
            alert('Please provide valid inputs')
                            //of signup class. So it will print out the error whose key is error
        }
    })
    e.preventDefault();
});
