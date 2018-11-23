$(function () {
  $('.pencil').on('submit', function (e) {
    e.preventDefault();
    $data = $(this).serializeArray();
    $flag = 0;
    $pencil = $(this).children().eq(3).children().eq(0).children().eq(0);
    $element = $(this).children().eq(2);
    $.each($data, function () {
      if (this.name == 'new_value') {
        $flag = 1;
        $x = $data[2].value;
        $y = this.value;
        data = {};
        data[$x] = $y;
        $.ajax({
          type: 'POST',
          url: '/amazon/updateuser/',
          data: data,
          success: function (response) {
            $pencil.replaceWith('<i class="fa fa-pencil" aria-hidden="true"></i>');
            $element.html($y);
          },

          fail: function (response) {
            console.log(response);
            console.log("Something went wrong");
          },
        });
      }
    });
    console.log($data);
    if ($flag == 0) {
      $element.html("<input class='form-control' type='text' name='new_value' value='" + $data[2].value + "' selected>");
      $element.children().eq(0).select();
      $(this).children().eq(3).children().eq(0).children().eq(0).replaceWith('<i class="fa fa-check" aria-hidden="true"></i>');
    }
  });
});
