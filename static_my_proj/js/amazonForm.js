$(document).ready(function() {
  // amazon account form stuff
  $('ul.multiselect-container').css('display', 'none');

  $('button.multiselect').on('click', function(evt){
    $('ul.multiselect-container').toggle();
  })
  $('#amz-cancel').on('click', function(evt){
    $('#amazonForm').modal('hide');
  })
  $( "#amazonRealForm" ).submit(function( event ) {
    event.preventDefault();
    amazonCheckConnect(event);
    console.log("done submit func");
  });
  $('#amzFormButton').on('click', function(evt){
    $('#amazonForm').modal('show');
  })
});

function amazonCheckConnect(event) {
  event.preventDefault();
  var d = $('form').serializeArray()
  var data = {};
  d.forEach(function fn(item, index){
    data[item.name] = item.value;
  });
  $url = '/amazon/add/';
  $.ajax({
    url: $url,
    data: data,
    type: 'POST',
    success: function(result){
      console.log("Successfully added")
      window.location.replace("http://127.0.0.1:8000/dashboard");
    },
    error: function(error){
      console.log(error);
    },
  });
}
