$(document).ready(function () {
    console.log( "ready!" );

    $('.decode').click(function () {
        console.log('decode')
        var id = $(this).attr("id").split('-');
        $('#expand-' + id[1]).slideToggle('slow', function () { });
        $(this).text( $(this).text() == 'Decode' ? 'Hide decode' : 'Decode');
    });

    $('#tbl_fltlist').find('tr').click(function () {
        SetFlightData('#mbr_request', $(this).children("td").html());

    })

    function SetFlightData(form, id) {
        $(form)[0].reset();
        var flight_data = flight_list[id];
        $.each(flight_data, function (key, value) {
            //console.debug(value);
            $('[name=' + key + ']', form).val(value);
            if ($('[name=' + key + ']', form).is(':checkbox')) {
                $('[name=' + key + ']', form).prop("checked", value)
            }

        });
    }

    if ($('#animated').length > 0) {
        var items = scan_json,
            delay = 2,
            $text = $('#animated');

        function loop(delay) {
            $.each(items, function (i, elm) {
                $text.delay(delay * 1E3).fadeOut();
                $text.queue(function () {
                    $text.html("<img src='data:image/png;base64," + items[i].fields.in_base64 + "'>");
                    $text.dequeue();
                });
                $text.fadeIn();
                $text.queue(function () {
                    if (i == items.length - 1) {
                        loop(delay);
                    }
                    $text.dequeue();
                });
            });
        }

        loop(delay);
    }

    if ($('#slideshow-container').length > 0) {
        var slideIndex = 0;
        showSlides();

        function showSlides() {
            var i;
            var slides = document.getElementsByClassName("mySlides");
            var dots = document.getElementsByClassName("dot");
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }
            slideIndex++;
            if (slideIndex > slides.length) {
                slideIndex = 1
            }
            for (i = 0; i < dots.length; i++) {
                dots[i].className = dots[i].className.replace(" active_dot", "");
            }
            slides[slideIndex - 1].style.display = "block";
            dots[slideIndex - 1].className += " active_dot";
            setTimeout(showSlides, 2000); // Change image every 2 seconds
        }
    }

    function archive() {
        alert('Call')

    }

})