let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['ke']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields

   // console.log(place);
   var geocoder = new google.maps.Geocoder()
   var address = document.getElementById('id_address').ariaValueMax
   console.log(address)

geocoder.geocode({'address': address}, function(results, status){
      // console.log('results=>', results)
       //console.log('status=>', status)
      if(status == google.maps.GeocoderStatus.OK){

    var latitude = results [0].geometry.location.lat();
    var longitude = results [0].geometry.location.lng();

    //console.log('latitude=>', latitude);
    //console.log('longitude=>', longitude);

      $('#id_latitude').val(latitude);
      $('#id_longitude').val(longitude);
      
      $('#id_address').val(address);

      }
});



    // loop through the address components and assign other address data
    for(var i=0; i<place.address_components.length; i++){
        for(var j=0; j<place.address_components[i].types.length; j++){

            //get country
            if(place_address_components[i].types[j] == 'country'){
                $('#id_country').val(place.address_components[i].long_name);
            }
           //get state
            if(place_address_components[i].types[j] == 'administrative_area_level_1'){
            $('#id_state').val(place.address_components[i].long_name);
            }
          //get city
            if(place_address_components[i].types[j] == 'locality'){
            $('#id_city').val(place.address_components[i].long_name);
            }
            //get pincode
            if(place_address_components[i].types[j] == 'postalcode'){
            $('#id_pin_code').val(place.address_components[i].long_name);
            }else{
                $('#id_pin_code').val('"');
            }

        }

    }


}


$(document).ready(function(){
    //add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        data = {
            'item_id': item_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                 console.log(response.cart_counter);
                 if(response.status == 'login_required'){
                    Swal(response.message, '', 'info').then(function() {
                        window.location.href = '/login/';
                    })
                 } if(response.status == 'error'){
                        swal(response.message, '', 'error')

                }else{
                    $('#cart_counter').html(response.cart_counter);
                    $('#qty-' + item_id).html(response.qty);

                    // subtotal tax and grandtotal
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )



            }
        }
        })
    })

    //place item qty on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty');
        $('#' +the_id).html(qty);
    })
    //decrease cart
        $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');


        data = {
            'item_id': item_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response.cart_counter);
                if(response.status == 'login_required'){
                    Swal(response.message, '', 'info').then(function() {
                        window.location.href = '/login/';
                    });
                }else if(response.status == 'error'){
                    console.log(response)
                }else{
                    $('#cart_counter').html(response.cart_counter);
                    $('#qty-' + item_id).html(response.qty);

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )   
                if(window.location.pathname == '/cart/'){
                    removeCartItem(response.qty, cart_id);
                    checkEmptyCart();

                }
            }
        }
        })
    })

    //delete cart
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        item_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).closest('li').attr('id').replace('cart_item-', '');

        $.ajax({
            type: 'GET',
            url: url,
            data: {
                'item_id': item_id
            },
            success: function(response){
              if(response.status == 'error'){
                    console.log(response)
                }else{
                    $('#cart_counter').html(response.cart_counter);
                    swal(response.status, response.message, 'success')

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']


                    )


                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                    
                }
            }
        })
    })

    //delete cart if the qty is zero
    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0){
            // remove cart item element
            document.getElementById('cart_item-' + cart_id).remove();
        }   
    }
   function checkEmptyCart(){
    var cartCounter = document.getElementById('cart_counter').innerHTML;
    if(cartCounter == 0){
        document.getElementById('empty-cart').style.display = 'block';
    }
   }

   //apply cart amounts
    function applyCartAmounts(subtotal, tax_dict, grand_total){
    if(window.location.pathname == '/cart/'){
        $('#subtotal').html(subtotal);
        $('#grand_total').html(grand_total);

        console.log(tax_dict)
        for(key1 in tax_dict){
            console.log(tax_dict[key1])
            for(key2 in tax_dict[key1]){
                
                $('#tax-'+key1).html(tax_dict[key1][key2])
     }
        }
            
            


    }
    }

// ADD OPENING HOURS
$('.add_hour').on('click', function (event) {
    event.preventDefault();

    var day = $('#id_day').val();
    var fromHour = $('#id_from_hour').val();
    var toHour = $('#id_to_hour').val();
    var isClosed = $('#id_is_closed').is(':checked');
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    var url = $('#add_hour_url').val();

    if (!day || (!isClosed && (!fromHour || !toHour))) {
        swal('Please fill all fields', '', 'info');
        return;
    }

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            day: day,
            from_hour: fromHour,
            to_hour: toHour,
            is_closed: isClosed ? 'True' : 'false',
            csrfmiddlewaretoken: csrfToken
        },
        success: function (response) {
            if (response.status !== 'success') {
                swal(response.message, '', 'error');
                return;
            }

            var details = response.is_closed === 'closed'
                ? 'Closed'
                : response.from_hour + ' - ' + response.to_hour;
            var html = '<tr id="hour-' + response.id + '">' +
                '<td><b>' + response.day + '</b></td>' +
                '<td>' + details + '</td>' +
                '<td><a href="#" class="delete_hour" data-url="' +
                '/accounts/vendor/opening-hours/delete/' + response.id + '/">Remove</a></td>' +
                '</tr>';

            $('.opening_hours tbody').append(html);
            $('#opening_hours')[0].reset();
        }
    });
});

// DELETE OPENING HOURS
$(document).on('click', '.delete_hour', function (event) {
    event.preventDefault();
    var link = $(this);
    var url = link.attr('data-url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            if (response.status === 'success') {
                $('#hour-' + response.id).remove();
            }
        }
    });
});

// document ready close

});
