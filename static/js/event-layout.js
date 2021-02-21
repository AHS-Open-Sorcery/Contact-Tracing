// Generate seats with starting positions
for (let i = 0; i < numSeats; i++) {
    editorContainer.append(`<div class="seat" id="seat-${i}" style="width: ${seatWidth}px;"><p>${i + 1}</p></div>`);
}

$(".seat").draggable({
    containment: "parent",
    start: (event, ui) => {
        // save coordinates for collision detection.
        let leftSave = $(ui.helper).css('left'), topSave = $(ui.helper).css('top');
        $(ui.helper).data({
            'leftSave': leftSave,
            'topSave': topSave,
        })
    },
    drag: (event, ui) => {
        let otherSeats = $(ui.helper).siblings('.seat');
        let leftSave = $(ui.helper).css('left'), topSave = $(ui.helper).css('top');

        if (!isSeatCollision($(ui.helper), otherSeats)) {
            $(ui.helper).data({
                'leftSave': leftSave,
                'topSave': topSave,
            });
        }
    },
    stop: (event, ui) => {
        let otherSeats = $(ui.helper).siblings('.seat');
        let leftSave = $(ui.helper).css('left'), topSave = $(ui.helper).css('top');

        if (isSeatCollision($(ui.helper), otherSeats)) {
            $(ui.helper).css({
                'top': $(ui.helper).data('topSave'),
                'left': $(ui.helper).data('leftSave')
            });
        } else {
            // Position is good, save new position
            $(ui.helper).data({
                'leftSave': leftSave,
                'topSave': topSave,
            })
        }
    }
});

function isSeatCollision(seatJQ, otherSeats) {
    let isOverlap = false;
    let diameter = seatJQ.outerWidth();
    let topStr = seatJQ.css('top'), leftStr = seatJQ.css('left');
    let centerY = parseFloat(topStr.substr(0, topStr.length - 2)),
        centerX = parseFloat(leftStr.substr(0, leftStr.length - 2));

    otherSeats.each((index, otherSeatDOM) => {
        let otherSeat = $(otherSeatDOM);

        let otherTopStr = otherSeat.css('top'), otherLeftStr = otherSeat.css('left');
        let otherCenterY = parseFloat(otherTopStr.substr(0, otherTopStr.length - 2)),
            otherCenterX = parseFloat(otherLeftStr.substr(0, otherLeftStr.length - 2));

        if (Math.sqrt(Math.pow(otherCenterX - centerX, 2) + Math.pow(otherCenterY - centerY, 2)) < diameter) {
            // There is an overlap!
            isOverlap = true;
            return false; // Breaks out of the each()
        }
    });

    return isOverlap;
}

for (let i = 0; i < numSeats; i++) {
    let currentRow = Math.floor(i / 10), currentCol = i % 10;
    let top = padding / 2 + currentRow * (seatWidth + padding), left = padding / 2 + currentCol * (seatWidth + padding);
    let thisSeat = $(`#seat-${i}`);

    thisSeat.css({
        'height': `${thisSeat.innerWidth()}px`,
        'top': `${top}px`,
        'left': `${left}px`
    });
}

function generateSeatLayout() {
    let layout = {
        'seats': []
    };

    for (let i = 0; i < numSeats; i++) {
        let thisSeat = $(`#seat-${i}`);
        let topStr = thisSeat.css('top'), leftStr = thisSeat.css('left');

        layout.seats.push({
            'number': i + 1,
            'top': parseFloat(topStr.substr(0, topStr.length - 2)),
            'left': parseFloat(leftStr.substr(0, leftStr.length - 2)),
            'occupied': false,
            'occupiedBy': null,
        })
    }

    return layout;
}

$('#save-button').click(() => {
    $('.seat').draggable('disable');
    $('#cancel-button').addClass('disabled');
    $('#save-button').css('pointer-events', 'none');

    $('#save-button').html('  <div class="preloader-wrapper small active">\n' +
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

    let currentLayout = generateSeatLayout();

    $.ajax({
        type: 'POST',
        url: '/event-layout',
        contentType: 'application/json',
        data: JSON.stringify({
            'layout': currentLayout,
            'id': eventID
        }),
        statusCode: {
            200: res => {
                window.location.replace(`/event-created?id=${eventID}`);
            }
        }
    });
});