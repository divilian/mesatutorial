
var StaticChartModule = function(width, height, name) {

    var canvas_tag = "<canvas width='" + width + "' height='" + height + "' ";
    canvas_tag += "style='border:2px solid'></canvas>";
    var canvas = $(canvas_tag)[0];
    $("#elements").append(canvas);
    var context = canvas.getContext("2d");

    var datasets = [{
        label: name,
        data: []
    }];

    var labels = [];
    
    var data = {
        labels: labels,
        datasets: datasets
    };

    var chart = new Chart(context, {type:'line', data:data});

    this.render = function(d) {
        datasets[0].data = d[1];
        data.labels = d[0];
        chart.update();
    };

    this.reset = function() {
        chart.destroy();
        chart = new Chart(context, {type:'line', data:data});
    };
        
};
