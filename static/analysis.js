$("#speech_button").click(function() {
	$("#speech_length_header").slideToggle();
	$("#show").toggle();
	$("#hide").toggle();
	$("#speech_length").slideToggle();
	$("#speech").slideToggle();
    $("#link").slideToggle();
});

$("#award").click(function() {
    var category = $("#award").text()
    var filtered_data = full_data.filter(function(d) { return d[8] === category })
    drawBarGraph(filtered_data)
});

$("#unfilter").click(function() {
    drawBarGraph(full_data)
});

$("#speech_length_header").click(function() {
	$("#speech_length_viz").slideToggle();
	$("#avg_speech_length_header").slideToggle();
    // $("#avg_category_length_header").slideToggle();
});

$("#avg_speech_length_header").click(function() {
	$("#avg_speech_length_viz").slideToggle();
	$("#speech_length_header").slideToggle();
    // $("#avg_category_length_header").slideToggle();
});

var margin = {top: 10, right: 20, bottom: 30, left: 80};
var width = 1300 - margin.left - margin.right;
var height = 400 - margin.top - margin.bottom;
var barPadding = 0.5;

var svg_length = d3.select("#speech_length").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg_avg = d3.select("#avg_speech_length").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function filter_out_honorary() {
    this.checked ? drawBarGraph(full_data) : drawBarGraph(non_honorary_data)
}

function filter_out_honorary_avg() {
    this.checked ? drawAvgBarGraph(avg_by_year_full) : drawAvgBarGraph(avg_by_year)
}

d3.select("#non_honorary_checkbox").on("change", filter_out_honorary);
d3.select("#avg_non_honorary_checkbox").on("change", filter_out_honorary_avg);

drawBarGraph(non_honorary_data);
drawAvgBarGraph(avg_by_year);

function drawBarGraph(data) {

    svg_length.selectAll("*").remove();

    var x = d3.time.scale()
        .range([0, width - 250]);

    var x0 = d3.time.scale()
        .range([0, width - 250]);

    var y = d3.scale.linear()
        .range([height, 0]);

    x.domain(d3.extent(data, function(d) { return +d[9]; }));
    x0.domain(d3.extent(data, function(d) { return d[11]; }));
    y.domain([0, d3.max(data, function(d) { return d[11]; })]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(10)
        .tickFormat(d3.format(""));

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10);

    var x0Axis = d3.svg.axis()
        .scale(x0)
        .orient("bottom")
        .ticks(10)
        .tickFormat(d3.format(""));

    var color = d3.scale.category20c();

    svg_length.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg_length.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    svg_length.selectAll(".bar")
        .data(data)
            .sort(function(a, b) { return d3.descending(a[11], b[11])})
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(+d[9]); })
        .attr("width", (width / data.length))
        .attr("y", function(d) { return y(d[11]); })
        .attr("height", function(d) { return height - y(d[11]); })
        .attr('fill', function(d) { 
            return color(d[8])
        })
        .on("mousemove", function(d) {
        	$("#winner").text(d[3])
        	$("#length").text(d[11])
        	$("#year").text(d[7])
        	$("#award").text(d[8])
        	$("#movie").text(d[2])
        	$("#speech").text(d[6])
            $("#link").attr("href", (d[10]))
        });

    var legendRectSize = 14;
    var legendSpacing = 2;

    var legend = svg_length.selectAll(".legend")
        .data(color.domain())
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) {
            var height = legendRectSize + legendSpacing;
            var offset = height * color.domain().length / 2;
            var horz = 1000;
            var vert = i * height - offset + 190;
            return "translate(" + horz + "," + vert + ")";
        });

    legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', color)
        .style('stroke', color);

    legend.append('text')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .text(function(d) { return d; });

    d3.select("#sort_checkbox").on("change", change);

        function change() {

            var transition = svg_length.transition().duration(50),
                delay = function(d, i) { return i/2; };

            transition.selectAll(".bar")
                .delay(delay)
                .attr("x", this.checked
                ? function(d) { return x0(d[11]); }
                : function(d) { return x(d[9]); })
                .attr("width", width/data.length)

            transition.select(".x.axis")
                .call(this.checked
                    ? x0Axis
                    : xAxis)
              .selectAll("g")
                .delay(delay);
        };
};

function drawAvgBarGraph(data) {

    svg_avg.selectAll("*").remove();
    var x = d3.time.scale()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    console.log(data)

    x.domain(d3.extent(data, function(d) { return d[0]; }));
    y.domain([0, d3.max(data, function(d) { return d[1]; })]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(5)
        .tickFormat(d3.format(""));

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10);

    svg_avg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg_avg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    svg_avg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(+d[0]); })
        .attr("width", (width / data.length))
        .attr("y", function(d) { return y(d[1]); })
        .attr("height", function(d) { return height - y(d[1]); })
        .on("mousemove", function(d) {
        	$("#avg_year").text(d[0])
        	$("#avg_length").text(d[1])
        });
};