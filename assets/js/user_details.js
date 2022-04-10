'use strict';
$(document).ready(function () {

    $('#js-minus-age').on('click', function() {
        js_minus('#user_age', 18);
    })

    $('#js-plus-age').on('click', function() {
        js_plus('#user_age', 151);
    })

    $('#js-minus-height').on('click', function() {
        js_minus('#user_height', 60);
    })

    $('#js-plus-height').on('click', function() {
        js_plus('#user_height', 248);
    })

    $('#js-minus-weight').on('click', function() {
        js_minus('#user_weight', 25);
    })

    $('#js-plus-weight').on('click', function() {
        js_plus('#user_weight', 300);
    })

    $('#submit-user-details').on('click', function() {
        var res = check_user_details();
        if (res['error'] === 0) {
            $('#submit-btn-text').addClass('d-none');
            $('#lds-submit-loader').removeClass('d-none');
            $('#submit-user-details').attr('disabled', true);
            $.ajax({
                type: "POST",
                headers: getHeader(),
                url: "/users/details/api/?_=" + new Date().getTime(),
                data: JSON.stringify({
                  age: $('#user_age').val().trim(),
                  gender: res['gender'][0],
                  height: $('#user_height').val().trim(),
                  weight: $('#user_weight').val().trim(),
                  activity: res['activity'],
                  medical: res['medical'],
                }),
                success: function (response) {
                    if (response['status'] == 'success') {
                        window.location.href = response['location'];
                    } else {
                      $('#notification').text(response['desc']);
                      $('#notification').removeClass('alert-soft-success');
                      $('#notification').addClass('alert-soft-danger');
                      $('#notification').removeClass('d-none');
                    }      
                }
              });
        }
    })

    function check_user_details() {
        var user_gender = (document.getElementById("user_gender")).getElementsByTagName("input");
        var user_activity = (document.getElementById("user_activity")).getElementsByTagName("input");
        var user_medical = (document.getElementById("user_medical")).getElementsByTagName("input");

        var gender = new Array();
        var activity = new Array();
        var medical = new Array();
        var err_cnt = 0;

        for (var i = 0; i < user_gender.length; i++) {
            if (user_gender[i].checked) {
                gender.push(user_gender[i].value);
            }
        }
        for (var i = 0; i < user_activity.length; i++) {
            if (user_activity[i].checked) {
                activity.push(user_activity[i].value);
            }
        }
        for (var i = 0; i < user_medical.length; i++) {
            if (user_medical[i].checked) {
                medical.push(user_medical[i].value);
            }
        }

        if (gender.length !== 1){
            err_cnt += 1;
            $('#popover_user_gender').removeClass('d-none');
        } else {
            $('#popover_user_gender').addClass('d-none');
        } 
        if (activity.length < 1) {
            err_cnt += 1;
            $('#popover_user_activity').removeClass('d-none');
        } else {
            $('#popover_user_activity').addClass('d-none');
        }
        if (medical.length < 1) {
            err_cnt += 1;
            $('#popover_user_medical').removeClass('d-none');
        } else {
            $('#popover_user_medical').addClass('d-none');
        }

        return {"error": err_cnt, "gender": gender, "medical": medical, "activity":activity};
        
    }

    function js_minus(input_tag, threshold) {
        if (parseInt($(input_tag).val()) > threshold) {
            $(input_tag).val(parseInt($(input_tag).val()) - 1);
        }
    }

    function js_plus(input_tag, threshold) {
        if (parseInt($(input_tag).val()) < threshold) {
            $(input_tag).val(parseInt($(input_tag).val()) + 1);
        }
    }

});