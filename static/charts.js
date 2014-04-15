var points = [
    [0, 0],
    [1, 0],
    [1, 1],
    [0.5, 1],
    [0, 0.5],
    [1.5, 0.5]
];

function drawPoints() {
    $.plot($("#my_chart"), [
        { data: points}
    ], {
        series: {
            lines: {
                show: true
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

    return 0;
}

function superTest() {

    var the_chart = $("#my_chart");

    drawPoints();
}

function addPoint(x, y) {

    points.push([x, y]);

    drawPoints();
}

function clear() {

    points = [];

    drawPoints();
}