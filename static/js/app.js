function loadData() {
  //d3.json('http://localhost:5000/data', showData);
}

function showData(data) {
  d3.select('body').selectAll('div.data-holder')
    .data(data['data'])
    .enter()
    .append('p').text(function(item) {
      return 'Item: ' + JSON.stringify(item);
    });
}

function showSvgLineChart() {
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 650 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

  var parseDate = d3.time.format("%Y-%m-%d").parse;
  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([height, 0]);
  var xAxis = d3.svg.axis().scale(x).orient("bottom");
  var yAxis = d3.svg.axis().scale(y).orient("left");

  var line = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.count); });

  var svg = d3.select("div.line-chart-holder").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.json('http://localhost:5000/data/count', function(error, result) {
    result = result['data'];
    data = [];
    for (date in result) {
      data.push({
        'date': parseDate(date),
        'count': result[date]
      });
    }

    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain(d3.extent(data, function(d) { return d.count; }));

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Player count");

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);
  });
}

function showC3LineChart() {
  d3.json('http://localhost:5000/data/count', function(error, result) {
    result = result['data'];
    dates = ['dates'];
    counts = ['counts'];
    for (date in result) {
      dates.push(date);
      counts.push(result[date]);
    }
    var chart = c3.generate({
        bindto: '.c3-line-chart-holder',
        data: {
          x: 'dates',
          columns: [ dates, counts ]
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%Y-%m-%d'
                }
            }
        }
    });
  });
}

function showHeatmap() {
  d3.json('http://localhost:5000/data/heatmap', function(error, result) {
    result = result['data'];
    console.log(result);
    var margin = { top: 50, right: 0, bottom: 80, left: 50 },
          width = 760 - margin.left - margin.right,
          height = 430 - margin.top - margin.bottom,
          gridSize = Math.floor(width / 24),
          legendElementWidth = gridSize*2,
          buckets = 9,
          colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"]; // alternatively colorbrewer.YlGnBu[9]

    for (var floor in result) {
          data = result[floor];
          dataX = []
          dataY = []
          for (var item in data) {
              dataX.push(item.x)
              dataY.push(item.y)
          }
          var colorScale = d3.scale.quantile()
              .domain([0, buckets - 1, d3.max(data, function (d) { return d.count; })])
              .range(colors);

          var svg = d3.select("div.heatmap-holder").append("h4")
              .text("Floor: " + floor);

          var svg = d3.select("div.heatmap-holder").append("svg")
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
              .append("g")
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          var xLabels = svg.selectAll(".xLabel")
              .data(dataX)
              .enter().append("text")
                .text(function (d) { return d; })
                .attr("x", 0)
                .attr("y", function (d, i) { return i * gridSize; })
                .style("text-anchor", "end")
                .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
                .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

          var yLabels = svg.selectAll(".yLabel")
              .data(dataY)
              .enter().append("text")
                .text(function(d) { return d; })
                .attr("x", function(d, i) { return i * gridSize; })
                .attr("y", 0)
                .style("text-anchor", "middle")
                .attr("transform", "translate(" + gridSize / 2 + ", -6)")
                .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

          var heatMap = svg.selectAll(".heatmap")
              .data(data)
              .enter().append("rect")
              .attr("x", function(d) { return (d.x - 1) * gridSize; })
              .attr("y", function(d) { return (d.y - 1) * gridSize; })
              .attr("rx", 4)
              .attr("ry", 4)
              .attr("class", "hour bordered")
              .attr("width", gridSize)
              .attr("height", gridSize)
              .style("fill", colors[0]);

          heatMap.transition().duration(1000)
              .style("fill", function(d) { return colorScale(d.count); });

          heatMap.append("title").text(function(d) {
            return "X:" + d.x + ",Y:" + d.y + " #" + d.count;
          });

          var legend = svg.selectAll(".legend")
              .data([0].concat(colorScale.quantiles()), function(d) { return d; })
              .enter().append("g")
              .attr("class", "legend");

          legend.append("rect")
            .attr("x", function(d, i) { return legendElementWidth * i; })
            .attr("y", height)
            .attr("width", legendElementWidth)
            .attr("height", gridSize / 2)
            .style("fill", function(d, i) { return colors[i]; });

          legend.append("text")
            .attr("class", "mono")
            .text(function(d) { return "≥ " + Math.round(d); })
            .attr("x", function(d, i) { return legendElementWidth * i; })
            .attr("y", height + gridSize);
      };
  });
}

$(document).ready(function() {
  showSvgLineChart();
  showC3LineChart();
  showHeatmap();
});
