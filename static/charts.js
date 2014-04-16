var points = [
    [0, 0],
    [1, 0],
    [1, 1],
    [0.5, 1],
    [0, 0.5],
    [1.5, 0.5]
];

var cubicPoints = [];

var zOrT = [0, 5, 5, 5, 5, 5];

function callPlot(data) {

    $.plot($("#my_chart"), [
        {
            color: 3,
            label: "Reference",
            data: data
        }
    ], {
        series: {
            lines: {
                show: true
            },
            points: {
                show: true,
                radius: 3
            },
            shadowSize: 0

        },
        xaxis: {
            zoomRange: [0.1, 10],
            panRange: [-10, 10]
        },
        yaxis: {
            zoomRange: [0.1, 10],
            panRange: [-10, 10]
        },
        zoom: {
            interactive: true
        },
        pan: {
            interactive: true
        }
    });
}

function drawPoints() {

    if ($("#planning").children(':selected').val() == 'points' || $("#planning").children(':selected').val() == 'reference') {
        callPlot(points);
    }
    else {

        cubicPoints = [];

        var T_planning = $('input[name="T"]').val();
        var K_planning = $('input[name="k"]').val();

        var planning_points = points.length;

        if (planning_points < 2 || T_planning <= 0 || K_planning <= 0) {
            callPlot([]);
            return;
        }

        var dN = T_planning * 20;

        var N = Math.floor(dN);

        var intervals = planning_points - 1;

        var max_count = N * intervals;

        if (max_count > 2000) {
            callPlot([]);
            return;
        }

        var i , j;

        for (j = 0; j < intervals; j++) {
            var x_i = points [j][0];
            var y_i = points [j][1];
            var theta_i = zOrT [j];

            var x_f = points [j + 1][0];
            var y_f = points [j + 1][1];
            var theta_f = zOrT [j + 1];

            var alfa_x = K_planning * Math.cos(theta_f) - 3 * x_f;
            var alfa_y = K_planning * Math.sin(theta_f) - 3 * y_f;

            var beta_x = K_planning * Math.cos(theta_i) + 3 * x_i;
            var beta_y = K_planning * Math.sin(theta_i) + 3 * y_i;


            for (i = 0; i < N; i++) {
                var s = i / N;

                cubicPoints.push([-( s - 1.0 ) * ( s - 1.0 ) * ( s - 1.0 ) * x_i + s * s * s * x_f + alfa_x * ( s * s ) * ( s - 1.0 ) + beta_x * s * ( ( s - 1.0 ) * ( s - 1.0 ) ),
                    -( s - 1.0 ) * ( s - 1.0 ) * ( s - 1.0 ) * y_i + s * s * s * y_f + alfa_y * ( s * s ) * ( s - 1.0 ) + beta_y * s * ( ( s - 1.0 ) * ( s - 1.0 ) )]);
            }
        }

        callPlot(cubicPoints);
    }
}

function initialize() {

    drawPoints();
    refreshSelect();

    $('a#calculate').click(function () {
        $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
            a: $('input[name="a"]').val(),
            b: $('input[name="b"]').val()
        }, function (data) {
            $("#result").text(data.result);
        });
    });
    $('a#restore').click(function () {
        drawPoints();
    });
    $('a#clear').click(function () {
        clear();
    });
    $('a#add').click(function () {
        addPoint($('input[name="x"]').val(), $('input[name="y"]').val()
            , $('input[name="t"]').val());
    });

    $('#execute').click(function () {

        var xArray = [];
        var yArray = [];

        for (var i = 0; i < points.length; i++) {
            xArray.push(points[i][0]);
            yArray.push(points[i][1]);
        }

        $.ajax({
            url: $SCRIPT_ROOT + "/execute",
            type: "POST",
            contentType: "application/json",
            processData: false,
            data: '{"k": ' + $('input[name="k"]').val() +
                ',"T": ' + $('input[name="T"]').val() +
                ',"planning": "' + $('#planning').val() + '"' +
                ',"zOrT": [' + zOrT + ']' +
                ',"xArray": [' + xArray + ']' +
                ',"yArray": [' + yArray + ']' +
                '}',
            dataType: "json",
            success: function (data) {
                $('#file').val(data.string);
                alert('command: ' + data.program);
            }
        });
    });

    $('a#remove').click(function () {
        var indexes = [];
        $("#points").children().filter(':selected').each(function () {
            indexes.push(this.value);
        });
        var newPoints = [];
        var newTimes = [];
        for (var i = 0; i < points.length; i++) {
            if (!has(indexes, i)) {
                //if ($.inArray(i, indexes) == -1) {
                //if (indexes.indexOf(i) == -1) {
                newPoints.push(points[i]);
                newTimes.push(zOrT[i]);
            }
        }

        points = newPoints;
        zOrT = newTimes;

        refreshSelect();
        drawPoints();
    });

    $('#planning').change(function () {
        drawPoints();
    });

    $('input[type="text"]').change(function () {
        if (isNaN($(this).val())) {
            alert('The data entered is invalid');
            this.value = 1;
        }
    });

}

function has(array, value) {

    for (var i = 0; i < array.length; i++) {
        if (array[i] == value) {
            return true;
        }
    }

    return false;
}

function addPoint(x, y, t) {

    points.push([x, y]);

    zOrT.push(t);

    refreshSelect();

    drawPoints();
}

function clear() {

    points = [];

    zOrT = [];

    cubicPoints = [];

    refreshSelect();

    drawPoints();
}

function refreshSelect() {

    var select = $('#points');

    select.children().remove();

    for (var i = 0; i < points.length; i++) {
        select.append(new Option(points[i].toString() + ',' + zOrT[i].toString(), i));
    }
}