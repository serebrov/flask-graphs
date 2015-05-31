function loadData() {
  d3.json('http://localhost:5000/data', showData);
}

function showData(data) {
  console.log(data);
  d3.selectAll('div.data-holder')
    .data(data)
    .enter()
    .append('div').text(function(item) {
      return 'Item: ' + item;
    });
}

$(document).ready(function() {
  loadData();
});
