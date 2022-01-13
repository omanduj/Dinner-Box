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
        url: "/user/foodpicker/",
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
        }
    })
    e.preventDefault();
});

$("form[name=restaurant_note]").submit(function(e){     //when form=X, on submit, do this

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/create-notes/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            var txt = resp['success'] + ' has been added'
            $('#add_note_response').html(txt);

            var txt = resp['Error']
            $('#add_note_response').html(txt);
        },
        error: function(resp) {
            console.log(resp);
            alert('Please provide valid inputs')
            $error.text(resp.responseJSON.error).removeClass('error--hidden');
        }
    })
    e.preventDefault();
});



$("form[name=delete_note]").submit(function(e){     //when form=X, on submit, do this

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/delete-note/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            location.reload();  
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass('error--hidden');
        }
    })
    e.preventDefault();
});

$("form[name=personal_picker]").submit(function(e){     //when form=X, on submit, do this

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/personal_picks/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);

            var name = 'Name: ' + Object.keys(resp)

            if (Object.keys(resp) != 'Error') {
                var rating = 'Rating: ' + resp[Object.keys(resp)]['rating']
                var note = 'Note: ' + resp[Object.keys(resp)]['note']
                $('#name').html(name);
                $('#rating').html(rating);
                $('#note').html(note);

            }  else {
                $('#name').html('');
                $('#rating').html('');
                $('#note').html('');
                $('#error').html(resp['Error'])
            }
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass('error--hidden');
        }
    })
    e.preventDefault();
});



$("form[name=token_instructions]").submit(function(e){     //when form=X, on submit, do this

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/token/instructions/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            $('#replace').html('How to use token service:');
            $('#replace2').html('Issue requests to the following endpoint: http://127.0.0.1:8000/auth/');
            $('#replace3').html('Define the headers as follows: -H "Authorization:{Bearer:my_token}"');
            $('#replace4').html('Then define the information you are passing in in the following format: --data "cost=$&rating=2"');
            $('#replace5').html('The final request should appear similar to:');
            $('#replace6').html('http://127.0.0.1:8000/auth/ -H "Authorization:{Bearer:my_token}" --data "cost=$&rating=2"');
            $('#replace7').html('Add curl if using as a CLI');
            $('#replace8').html('You will have 90 minutes before the token you have obtained expires, but you can reapply for more!');
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass('error--hidden');
        }
    })
    e.preventDefault();
});
// $("form[name=order_notes]").submit(function(e){     //when form=X, on submit, do this
//
//     var $form = $(this);
//     var $error = $form.find(".error");
//     var data = $form.serialize();
//
//     $.ajax({
//         url: "/user/order/",
//         type: "POST",
//         data: data,
//         dataType: "json",
//         success: function(resp) {
//             console.log(resp);
//             $('#add_note_response').html(resp);
//         },
//         error: function(resp) {
//             console.log(resp);
//             $error.text(resp.responseJSON.error).removeClass('error--hidden');
//         }
//     })
//     e.preventDefault();
// });
