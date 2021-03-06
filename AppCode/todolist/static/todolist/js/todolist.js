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

function deleteRow(row) {
  document.getElementById("tasks-table-body").deleteRow(row.parentNode.parentNode.rowIndex);
  if(document.getElementById("tasks-table-body").rows.length == 0)
    document.getElementById("no-tasks").removeAttribute("hidden");
}

$(document).ready(function() {
  taskRerenderURLString = window.location.origin + "/todolist/rerender/";
  $(".add-task-button").click(function(e) {
    taskCreateURLString = window.location.origin + "/todolist/task-create/";
    $(".task-create-modal-body").load(taskCreateURLString);
  });
  
    $("#task-form-submit").click(function(e) {
      var frm = $("#task-create-form");
      $.ajaxSetup({
        headers: { "X-CSRFToken": '{{csrf_token}}' }
      });
      $(".task-create-close-button").click();
      e.preventDefault();
      $.ajax({
        type: frm.attr('method'),
        url: taskCreateURLString,
        data: frm.serialize(),
        success: function(data) {
          console.log('Submission was successful.');
          $(".subtasks-table").load(taskRerenderURLString);
        },
        error: function(data) {
          console.log('An error occurred.');
        },
      });
    });

  $(".edit-button").click(function(e) {
    var taskId = $(this).attr('data-id');
    taskEditURLString = window.location.origin + "/todolist/task-edit/" + taskId + "/";

    var currentIds = $(this).closest("tr").find("td");
    var cell0 = $(currentIds).eq(0).text().trim();
    var cell1 = $(currentIds).eq(1).text().trim();
    var cell2 = $(currentIds).eq(2).text().trim();
    $("#edit-name").val(cell0);
    $("#edit-due_date").val(cell1);
    $("#edit-due_time").val(cell2);
    $("#TaskEditModal").modal('toggle');
  });

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
        $(".subtasks-table").load(taskRerenderURLString);
        $("#TaskEditModal").modal('toggle');
        $('.modal-backdrop').remove();
      },
      error: function(data) {
        console.log('An error occurred.');
      },
    });
  });

  $(".delete-button").click(function(e) {
    taskDeleteURLString = window.location.origin + "/todolist/task-delete/" + $(this).attr('data-id') + "/";
    document.getElementById("TaskDeleteModalLabel").innerHTML = "Are you sure you want to delete '" + $(this).closest("tr").find("td").eq(0).text().trim() + "'?";
  });

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
        $("#delete-task-cancel").click();
        $(".subtasks-table").load(taskRerenderURLString);
      },
      error: function(data) {
        console.log("An error occurred");
      },
    });
  });

  $(".table-row").click(function(e) {
    pageCurrentId = $(this).data('id');
    var currentObj = $(this).closest("tr").find("td");
    pageCurrentTask = $(currentObj).eq(0).text().trim();
    var subtaskViewURL = window.location.origin + "/todolist/subtasks/" + pageCurrentId;
    console.log(subtaskViewURL);
    $('.subtask-view-modal-body').load(subtaskViewURL);
    $("SubtaskViewModal").modal("toggle");
  });

  $("#add-subtask-button").click(function(e) {
    createSubtaskURL = window.location.origin + "/todolist/subtask-create/" + pageCurrentId + "/";
    console.log(createSubtaskURL);
    $(".subtask-close-button").click();
    $(".subtask-create-modal-body").load(createSubtaskURL);
    $("#SubtaskViewModal").modal("hide");
    $("#SubtaskCreateModal").modal("toggle");
  });

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
    var subtaskRerenderViewURL = window.location.origin + "/todolist/subtasks-rerender/" + pageCurrentId;
    console.log(subtaskRerenderViewURL);
    $(".subtask-view-modal-body").load(subtaskRerenderViewURL);
    $("#SubtaskViewModal").modal("show");
  });

  $(".subtask-close-button").click(function(e) {
    $("#SubtaskViewModal").modal("hide");
  });
});