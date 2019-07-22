$(document).ready(function(){
  console.log('document is ready');

  $('#inference').click(async function(){
    console.log('button was clicked');

    const kill = parseFloat($('#kill').val());
    const assist = parseFloat($('#assist').val());
    const death = parseFloat($('#death').val());
    const special = parseFloat($('#special').val());
    const inked = parseFloat($('#inked').val());
    const data = {
      kill,
      assist,
      death,
      special,
      inked
    }
    console.log(data)

    const response = await $.ajax('/inference',{
      data: JSON.stringify(data),
      method: "post",
      contentType: "application/json"
    })
    console.log(response)
    $('#score').val(response.prediction)

  })

})
