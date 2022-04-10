'use strict';
$(document).ready(function () {


  $('#login_section_toggle').on('click', function() {
    $('#welcome_section').addClass('d-none');
    $('#registration_section').addClass('d-none');
    $('#login_section').removeClass('d-none');
    $('#notification').addClass('d-none');
  })

  $('#registration_section_toggle').on('click', function() {
    $('#welcome_section').addClass('d-none');
    $('#login_section').addClass('d-none');
    $('#registration_section').removeClass('d-none');
    $('#notification').addClass('d-none');
  })

  $('#login_section_toggle_register').on('click', function() {
    $('#welcome_section').addClass('d-none');
    $('#registration_section').addClass('d-none');
    $('#login_section').removeClass('d-none');
    $('#notification').addClass('d-none');
  })

  $('#registration_section_toggle_signin').on('click', function() {
    $('#welcome_section').addClass('d-none');
    $('#login_section').addClass('d-none');
    $('#registration_section').removeClass('d-none');
    $('#notification').addClass('d-none');
  })

  $('#signin-btn-submit').on('click', function () {
    var user = $('#email_id').val().trim();
    var pswd = $('#current_password').val().trim();

    if (user == '' && pswd == '') {
      $('#popover_email_id').removeClass('d-none');
      $('#popover_current_password').removeClass('d-none');
    } else if (user == '') {
      $('#popover_email_id').removeClass('d-none');
      $('#popover_current_password').addClass('d-none');
    } else if (pswd == '') {
      $('#popover_email_id').addClass('d-none');
      $('#popover_current_password').removeClass('d-none');
    } else if (user != '' && pswd != '') {
      $('#signin-btn-submit').attr('disabled', true);
      $('#signin-btn-text').addClass('d-none');
      $('#lds-submit-loader').removeClass('d-none');
      $('#popover_email_id').addClass('d-none');
      $('#popover_current_password').addClass('d-none');
      $('#registration_section_toggle_signin').attr('disabled', true);
      $.ajax({
        type: "POST",
        headers: {
          'Content-Type':'application/json',
          'accept': 'application/json',
        },
        url: "/users/login/api/",
        data: JSON.stringify({
          email_id: user,
          password: pswd
        }),
        success: function (response) {
          var tmpData = response;

          if (tmpData['status'] == 'success') {
            window.location.href = tmpData['location'];
          } else {
            $('#notification').text(response['desc']);
            $('#notification').removeClass('alert-soft-success');
            $('#notification').addClass('alert-soft-danger');
            $('#notification').removeClass('d-none');
            
            $('#signin-btn-text').removeClass('d-none');
            $('#lds-submit-loader').addClass('d-none');
            $('#signin-btn-submit').attr('disabled', false);
            $('#registration_section_toggle_signin').attr('disabled', false);
          }
        }
      });
    }
  });

  $(document).on('click', '#register-btn-submit', function () {
    if (checkNewUser() == 0) {
      $('#register-btn-text').addClass('d-none');
      $('#lds-register-loader').removeClass('d-none');
      $('#register-btn-submit').attr('disabled', true);
      $('#login_section_toggle_register').attr('disabled', true) ;
      $.ajax({
        type: "POST",
        headers: getHeader(),
        url: "/users/register/api/?_=" + new Date().getTime(),
        data: JSON.stringify({
          full_name: $('#full_name').val().trim(),
          email_id: $('#new_email_id').val().trim(),
          password: $('#confirm_password').val().trim()
        }),
        success: function (response) {
            if (response['status'] == 'success') {
              $('#notification').removeClass('alert-soft-danger');
              $('#notification').addClass('alert-soft-success');
              $('#registration_form')[0].reset();
              $('#notification').text(response['desc']);
              $('#notification').removeClass('d-none');
            } else {
              $('#notification').text(response['desc']);
              $('#notification').removeClass('alert-soft-success');
              $('#notification').addClass('alert-soft-danger');
              $('#notification').removeClass('d-none');
            }
            $('#register-btn-text').removeClass('d-none');
            $('#lds-register-loader').addClass('d-none');
            $('#register-btn-submit').attr('disabled', false);
            $('#login_section_toggle_register').attr('disabled', false);       
        }
      });
    }
  });

  function checkNewUser() {
    var ecnt = 0;
    if ($('#full_name').val().trim() == '') {
      ecnt += 1;
      $('#popover_full_name').removeClass('d-none');
      $('#popover_full_name').html('Please enter your full name.')
    } else if (!$('#full_name').val().trim().match(/^[a-zA-Z ]*$/)) {
      ecnt += 1;
      $('#popover_full_name').removeClass('d-none');
      $('#popover_full_name').html('Field should contain only alphabetic characters.')
    } else if (($('#full_name').val().trim()).length < 5) {
      ecnt += 1;
      $('#popover_full_name').removeClass('d-none');
      $('#popover_full_name').html('Please provide atleast 5 alpha characters.')
    } else {
      $('#popover_full_name').addClass('d-none');
    }

    if ($('#new_email_id').val().trim() == '') {
      ecnt += 1;
      $('#popover_new_email_id').removeClass('d-none');
      $('#popover_new_email_id').html('Please enter an email address.')
    } else if (!validateEmail($('#new_email_id').val())) {
      ecnt += 1;
      $('#popover_new_email_id').removeClass('d-none');
      $('#popover_new_email_id').html('Please enter valid email address.')
    } else {
      $('#popover_new_email_id').addClass('d-none');
    }

    if ($('#new_password').val().trim() == '') {
      ecnt += 1;
      $('#popover_new_password').removeClass('d-none');
      $('#popover_new_password').html('Please enter the new password.')
    } else if ($('#new_password').val().length < 8) {
      ecnt += 1;
      $('#popover_new_password').removeClass('d-none');
      $('#popover_new_password').html('Please enter the valid password.')
    } else {
      $('#popover_new_password').addClass('d-none');
    }

    if ($('#confirm_password').val().trim() == '') {
      ecnt += 1;
      $('#popover_confirm_password').removeClass('d-none');
      $('#popover_confirm_password').html('Please enter the confirm password.')
    } else if ($('#confirm_password').val().length < 8) {
      ecnt += 1;
      $('#popover_confirm_password').removeClass('d-none');
      $('#popover_confirm_password').html('Please enter the valid password.')
    } else if ($('#confirm_password').val().trim() !== $('#new_password').val().trim()) {
      ecnt += 1;
      $('#popover_confirm_password').removeClass('d-none');
      $('#popover_confirm_password').html('Confirm pasword doesn\'t match with New password.')
    } else {
      $('#popover_confirm_password').addClass('d-none');
    }

    return ecnt;
  }

  function validateEmail($email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,6})?$/;
    return emailReg.test($email);
  }

});