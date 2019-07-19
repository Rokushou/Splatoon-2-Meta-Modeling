$(document).ready(function(){
  console.log('document is ready')

  $('#inference').click(async function(){
    console.log('button was clicked')

    const cylinders = parseFloat($('#cylinders').val())
    const horsepower = parseFloat($('#horsepower').val())
    const weight = parseFloat($('#weight').val())

    const data = {
      cylinders,
      horsepower,
      weight
    }
    console.log(data)

    const response = await $.ajax('/inference',{
      data: JSON.stringify(data),
      method: "post",
      contentType: "application/json"
    })
    console.log(response)
    $('#mpg').val(response.prediction)
  })
})
