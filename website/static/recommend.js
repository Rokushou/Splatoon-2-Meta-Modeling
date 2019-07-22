$(document).ready(function(){
  console.log('document is ready');

  $('#submit').click(async function(){
    console.log('button was clicked');

    const weapon = $('#weapon').val();
    const mode = $('#mode').val();
    const data = {
      weapon,
      mode
    }
    console.log(data)

    const response = await $.ajax('/rec',{
      data: JSON.stringify(data),
      method: "post",
      contentType: "application/json"
    })
    console.log(response)
    $('#rec').val(response.prediction)

  })
})
