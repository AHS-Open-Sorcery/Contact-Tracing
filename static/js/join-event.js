let lastSelectedSeat = null;


// Generate seats with starting positions
for (let i = 0; i < numSeatsInEvent; i++) {
    editorContainer.append(`<div class="seat ${layout[i].occupied ? '' : 'available'}" id="seat-${i}" style="height: ${seatWidth}px; width: ${seatWidth}px; top: ${layout[i].top}px; left: ${layout[i].left}px;"><p>${i + 1}</p></div>`);
}

$('.seat.available').on('click', '*', (event) => {
    let thisSeat = $(event.target);

    if (!thisSeat.hasClass('seat')) {
        thisSeat = thisSeat.closest('.seat');
    }

    if (lastSelectedSeat != null) {
        lastSelectedSeat.removeClass('selected');
        lastSelectedSeat.css('pointer-events', 'all');
        lastSelectedSeat.children('p').first().html(parseInt(lastSelectedSeat.attr('id').split('-')[1]) + 1);
    }

    thisSeat.children('p').first().html('<i class="material-icons">check</i>');

    thisSeat.addClass('selected');
    thisSeat.css('pointer-events', 'none');
    lastSelectedSeat = thisSeat;

    $('#select-button').removeClass('disabled');
});

$('#select-button').click(() => {
    $('.seat').css('pointer-events', 'none');
    $('#cancel-button').addClass('disabled');
    $('#select-button').css('pointer-events', 'none');

    $('#select-button').html('  <div class="preloader-wrapper small active">\n' +
        '    <div class="spinner-layer spinner-white-only">\n' +
        '      <div class="circle-clipper left">\n' +
        '        <div class="circle"></div>\n' +
        '      </div><div class="gap-patch">\n' +
        '        <div class="circle"></div>\n' +
        '      </div><div class="circle-clipper right">\n' +
        '        <div class="circle"></div>\n' +
        '      </div>\n' +
        '    </div>\n' +
        '  </div>');

    $.ajax({
        type: 'POST',
        url: '/join-event-endpoint',
        contentType: 'application/json',
        data: JSON.stringify({
            'seat_number': parseInt(lastSelectedSeat.attr('id').split('-')[1]) + 1,
            'id': eventID
        }),
        statusCode: {
            200: res => {
                window.location.replace(`/event-joined?id=${eventID}`);
            }
        }
    });
});