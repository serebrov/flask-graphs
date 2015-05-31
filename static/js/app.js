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

$(document).ready(function() {
  showSvgLineChart();
  showC3LineChart();
});
