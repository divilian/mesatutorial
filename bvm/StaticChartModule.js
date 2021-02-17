
var StaticChartModule = function(width, height, name) {

    var canvas_tag = "<canvas width='" + width + "' height='" + height + "' ";
    canvas_tag += "style='border:1px dotted'></canvas>";
    var canvas = $(canvas_tag)[0];
    $("#elements").append(canvas);
    var context = canvas.getContext("2d");

    var datasets = [{
        label: name,
        data: []
    }];

    var labels = [];
    for (var i=10; i<110; i+=10) {
        labels.push(i)
    }
    
    var data = {
        labels: labels,
        datasets: datasets
    };

    var chart = new Chart(context, {type:'line', data:data});

    this.render = function(data) {
        datasets[0].data = data;
        chart.update();
    };

    this.reset = function() {
        chart.destroy();
        chart = new Chart(context, {type:'line', data:data});
    };
        
};
