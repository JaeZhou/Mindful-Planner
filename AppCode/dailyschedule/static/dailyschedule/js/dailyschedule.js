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

  $(".add-task-button").click(function(e) {
    taskCreateURLString = window.location.origin + "/dailyschedule/task-create/";
    $(".task-create-modal-body").load(taskCreateURLString);
  
    $.ajaxSetup({
      headers: { "X-CSRFToken": '{{csrf_token}}' }
    });
  
    $("#task-form-submit").click(function(e) {
      var frm = $("#task-create-form");
      e.preventDefault();
      $.ajax({
        type: frm.attr('method'),
        url: taskCreateURLString,
        data: frm.serialize(),
        success: function(data) {
          console.log('Submission was successful.');
        },
        error: function(data) {
          console.log('An error occurred.');
        },
      });
      $(".task-create-close-button").click();
    });
  });

  $(".edit-button").click(function(e) {
    var taskId = $(this).attr('data-id');
    var taskEditURLString = window.location.origin + "/dailyschedule/task-edit/" + taskId + "/";

    var currentIds = $(this).closest("tr").find("td");
    var cell0 = $(currentIds).eq(0).text().trim();
    var cell1 = $(currentIds).eq(1).text().trim();
    var cell2 = $(currentIds).eq(2).text().trim();
    $("#edit-name").val(cell0);
    $("#edit-due_date").val(cell1);
    $("#edit-due_time").val(cell2);
    $("#TaskEditModal").modal('toggle');

    $("#edit-task-form-submit").click(function(e) {
      $.ajaxSetup({
        headers: { "X-CSRFToken": '{{csrf_token}}' }
      });

      var frm2 = $("#task-edit-form");
      console.log(frm2.serialize());
      e.preventDefault();
      $.ajax({
        type: frm2.attr('method'),
        url: taskEditURLString,
        data: frm2.serialize(),
        success: function(data) {
          console.log('Submission was successful.');
        },
        error: function(data) {
          console.log('An error occurred.');
        },
      });
    });
  });

  $(".delete-button").click(function(e) {
    taskDeleteURLString = window.location.origin + "/dailyschedule/task-delete/" + $(this).attr('data-id') + "/";
    document.getElementById("TaskDeleteModalLabel").innerHTML = "Are you sure you want to delete '" + $(this).closest("tr").find("td").eq(0).text().trim() + "'?";

    $("#delete-task-form-submit").click(function(e) {
      e.preventDefault();
      $.ajax({
        type: "POST",
        url: taskDeleteURLString,
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        success: function(data) {
          console.log("Submission was successful");
        },
        error: function(data) {
          console.log("An error occurred");
        },
      });
    });
  });

  $(".table-row").click(function(e) {
    pageCurrentId = $(this).data('id');
    var currentObj = $(this).closest("tr").find("td");
    pageCurrentTask = $(currentObj).eq(0).text().trim();
    var subtaskViewURL = window.location.origin + "/dailyschedule/subtasks/" + pageCurrentId;
    console.log(subtaskViewURL);
    $('.subtask-view-modal-body').load(subtaskViewURL);
    $("SubtaskViewModal").modal("toggle");
  });

  $("#add-subtask-button").click(function(e) {
    var createSubtaskURL = window.location.origin + "/dailyschedule/subtask-create/" + pageCurrentId + "/";
    console.log(createSubtaskURL);
    $(".close-button").click();
    $(".subtask-create-modal-body").load(createSubtaskURL);
    $("#SubtaskViewModal").modal("hide");
    $("#SubtaskCreateModal").modal("toggle");

    $("#subtask-form-submit").click(function(e) {
      var frm4 = $("#subtask-create-form");
      $("#SubtaskCreateModal").modal("toggle");   
      e.preventDefault();
      $.ajax({
        type: frm4.attr('method'),
        url: createSubtaskURL,
        data: frm4.serialize(),
        success: function(data) {
          console.log('Submission was successful.');
        },
        error: function(data) {
          console.log('An error occurred.');
        },
      });
      $("#SubtaskViewModal").modal("show");
    });
  }); 


  // START OF EVENT SCRIPTS

  // Event Form Start //
  var eventfrm = $('#event-form');    

  $( document ).ready(function() {
    $.ajaxSetup({
      headers: { "X-CSRFToken": '{{csrf_token}}' }
    });

    $("#event-form-submit").click(function(e) {
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
  });

  $(document).ready(function() {
    $(".edit-button-event").click(function() {
      var currentTds = $(this).closest("tr").find("td");
      var cell0 = $(currentTds).eq(0).text().trim();
      var cell1 = $(currentTds).eq(1).text().trim();
      var cell2 = $(currentTds).eq(2).text().trim();
      var cell3 = $(currentTds).eq(3).text().trim();
      var cell4 = $(currentTds).eq(4).text().trim();
      $("#edit-title").val(cell0);
      $("#edit-day").val(cell1);
      $("#edit-start_time").val(cell2);
      $("#edit-end_time").val(cell3);
      $("#edit-description").val(cell4);
      $("#EventEditModal").modal('show');
    });
  });
  // Event Edit End //

  // Event Edit Start //
  var eventfrm2 = $("#edit-event-form");

  $(".edit-button-event").click(function(e) {
  var eventId = $(this).attr('data-id');

  var editURLString = window.location.origin + "/dailyschedule/event-edit/" + eventId + "/";
  //var edit2 = edit.concat(taskId, "/");
  var deleteURLString = window.location.origin + "/dailyschedule/event-delete/" + eventId + "/";
  //var delete2 = delete3.concat(taskId, "/");

  $(document).ready(function() {
    $.ajaxSetup({
      headers: { "X-CSRFToken": '{{csrf_token}}' }
    });

    $("#edit-event-form-submit").click(function(e) {
      e.preventDefault();
      $.ajax({
        type: eventfrm2.attr('method'),
        // url: temp3,
        url: editURLString,
        data: eventfrm2.serialize(),
        success: function(data) {
          console.log('Submission was successful.');
        },
        error: function(data) {
          console.log('An error occurred.');
        },
      });
    });
  });
  });
  // Event Edit End //

  // Event Delete Start //
  var eventfrm3 = $('#delete-event-form');

  $(".delete-button-event").click(function(e) {
    var currentId = $(this).attr('data-id');
    var currentObject = $(this).closest("tr").find("td");
    var currentName = $(currentObject).eq(0).text().trim();
    document.getElementById("EventDeleteModalLabel").innerHTML = "Are you sure you want to delete '" + currentName + "'?";
    deleteString = window.location.origin + "/dailyschedule/event-delete/" + currentId + "/";

    $(document).ready(function() {
      $.ajaxSetup({
        headers: { "X-CSRFToken": '{{csrf_token}}' }
      });

      $("#delete-event-form-submit").click(function(e) {
        e.preventDefault();
        $.ajax({
          type: eventfrm3.attr('method'),
          url: deleteString,
          success: function(data) {
            console.log('Submission was successful.');
          },
          error: function(data) {
            console.log('An error occurred.');
          },
        });
      });
    });
  });
  // Event Delete Start //
});
