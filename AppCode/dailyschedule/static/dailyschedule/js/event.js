var pageCurrentId;
var pageCurrentTask;

function getCurrentId() {
  return pageCurrentId;
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

$(document).ready(function() {
    
    // START OF EVENT SCRIPTS

  // Event Form Start //
  // var eventfrm = $('#event-form');   
  $("#event-form-submit").click(function(e) {
    var eventfrm = $("#event-create-form");
    $.ajaxSetup({
      headers: { "X-CSRFToken": '{{csrf_token}}' }
    });
    $(".event-create-close-button").click();
    e.preventDefault();
    $.ajax({
      type: eventfrm.attr('method'),
      url: eventfrm.attr('action'),
      data: eventfrm.serialize(),
      success: function(data) {
        console.log('Submission was successful.');

      },
      error: function(data) {
        console.log('An error occurred.');
      },
    });
  });

  $(".edit-button-event").click(function(e) {
    var eventId = $(this).attr('data-id');
    eventEditURLString = window.location.origin + "/dailyschedule/event-edit/" + eventId + "/";

    var currentIds = $(this).closest("tr").find("td");
    var cell0 = $(currentIds).eq(0).text().trim();
    var cell1 = $(currentIds).eq(1).text().trim();
    var cell2 = $(currentIds).eq(2).text().trim();
    var cell3 = $(currentIds).eq(3).text().trim();
    var cell4 = $(currentIds).eq(4).text().trim();
    $("#edit-title").val(cell0);
    $("#edit-day").val(cell1);
    $("#edit-start_time").val(cell2);
    $("#edit-end_time").val(cell3);
    $("#edit-description").val(cell4);
    $("#EventEditModal").modal('toggle');
  });

  $("#edit-event-form-submit").click(function(e) {
    $.ajaxSetup({
      headers: { "X-CSRFToken": '{{csrf_token}}' }
    });

    var frm2 = $("#event-edit-form");
    console.log(frm2.serialize());
    e.preventDefault();
    $.ajax({
      type: frm2.attr('method'),
      url: eventEditURLString,
      data: frm2.serialize(),
      success: function(data) {
        console.log('Submission was successful.');
        $("#eventEditModal").modal('toggle');
        $('.modal-backdrop').remove();
      },
      error: function(data) {
        console.log('An error occurred.');
      },
    });
  });


  $(".delete-button-event").click(function(e) {
    eventDeleteURLString = window.location.origin + "/dailyschedule/event-delete/" + $(this).attr('data-id') + "/";
    document.getElementById("EventDeleteModalLabel").innerHTML = "Are you sure you want to delete '" + $(this).closest("tr").find("td").eq(0).text().trim() + "'?";
  });

  $("#delete-event-form-submit").click(function(e) {
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: eventDeleteURLString,
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      success: function(data) {
        console.log("Submission was successful");
        $("#delete-event-cancel").click();
      },
      error: function(data) {
        console.log("An error occurred");
      },
    });
  });
});